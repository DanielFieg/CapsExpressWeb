<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Marcas;
use App\Models\User;
use Symfony\Component\HttpFoundation\Request;
use Illuminate\Support\Facades\Log;
use App\Models\SearchResult;
use App\Models\PalavrasProibidas;
use Illuminate\Support\Facades\Auth;

class AdminController extends Controller
{
    public function viewMarcas()
    {
        return view('formMarcas');
    }

    public function createMarcas(Request $request)
    {
        Log::info($request);
        // Crie a marca no banco de dados
        $marca = Marcas::create([
            'marca' => $request->input('marca'),
        ]);

        // Retorne uma resposta de sucesso para o frontend
        return response()->json(['success' => true, 'message' => 'Marca cadastrada com sucesso!', 'marca' => $marca]);
    }

    public function viewPalavrasProib(){
        return view('relPalavrasProibidas');
    }

    public function listPalavrasProib(){
        $palavrasProibidas = PalavrasProibidas::orderBy('id', 'asc')->get();
        return $palavrasProibidas;
    }

    public function createPalavra(Request $request) {
        // Validação da entrada
        $validated = $request->validate([
            'palavra' => 'required|string|max:255', // Ajuste a validação conforme necessário
        ]);
    
        // Verifica se a palavra já existe no banco de dados
        $palavraExistente = PalavrasProibidas::where('palavra_proibida', $request->input('palavra'))->first();
    
        if ($palavraExistente) {
            // Retorna um erro se a palavra já estiver cadastrada
            return response()->json([
                'success' => false,
                'message' => 'Esta palavra proibida já está cadastrada!'
            ], 400);
        }
    
        // Criação do novo registro se a palavra não existir
        $palavrasProibidas = PalavrasProibidas::create([
            'palavra_proibida' => $request->input('palavra'),
        ]);
    
        // Retorna uma resposta de sucesso
        return response()->json([
            'success' => true, 
            'message' => 'Palavra Proibida cadastrada com sucesso!', 
            'marca' => $palavrasProibidas
        ]);
    }

    public function destroy($id){
        $palavra = PalavrasProibidas::find($id);

        if (!$palavra) {
            return response()->json(['message' => 'Palavra não encontrada.'], 404);
        }

        $palavra->delete();

        return response()->json(['message' => 'Palavra deletada com sucesso.']);
    }


    public function listMarcas(){
        $marcas = Marcas::all();
        return $marcas;
    }

    public function searchMarcas(Request $request) {
        ini_set('max_execution_time', 600);
    
        $id = $request->query('id');
        $marca = $request->query('marca');
        Log::info("ID: " . $id);
        Log::info("Marca: " . $marca);
    
        // Atualize o caminho para o Python se necessário
        $command = escapeshellcmd("python3 scripts/ExtractorLinkByDuck.py " . escapeshellarg($marca));
        Log::info("Command: " . $command);
    
        $descriptorspec = [
            0 => ["pipe", "r"],
            1 => ["pipe", "w"],
            2 => ["pipe", "w"]
        ];
    
        $process = proc_open($command, $descriptorspec, $pipes);
        Log::info($process);
    
        if (is_resource($process)) {
            fclose($pipes[0]);
            $output = stream_get_contents($pipes[1]);
            Log::info("Raw JSON output: " . $output);

            fclose($pipes[1]);
    
            $errorOutput = stream_get_contents($pipes[2]);
            Log::info($errorOutput);
            fclose($pipes[2]);
    
            $returnValue = proc_close($process);
            Log::info("Return Value: " . $returnValue);
    
            if ($returnValue === 0) {
                $links = json_decode($output, true);
                Log::info($links);
    
                if (json_last_error() === JSON_ERROR_NONE) {
                    Log::info("Links: " . print_r($links, true));
    
                    $rpaResults = [];
                    foreach ($links as $link) {
                        $linkUrl = $link['link'];
                        if (isset($link['error'])) {
                            Log::error("Erro no link: " . $link['error']);
                            $rpaResults[] = [
                                'link' => $linkUrl,
                                'message' => 'Erro ao abrir o link. Verifique o URL ou tente novamente mais tarde.'
                            ];
                            continue;
                        }
                        $rpaResult = $this->executeRpaForLink($linkUrl);
                        Log::info($rpaResult);
                        Log::info("Resultado na função dos links: " . print_r($rpaResult, true));
    
                        if ($rpaResult['status'] === 'error') {
                            Log::error("Erro na função dos links: " . $rpaResult['message']);
                            $rpaResults[] = [
                                'link' => $linkUrl,
                                'message' => 'Erro ao processar o link.'
                            ];
                            continue;
                        }
                        $rpaResults = array_merge($rpaResults, $rpaResult['data']);
    
                        // Salvar resultados individuais
                        foreach ($rpaResult['data'] as $result) {
                            if (isset($result['message']) && $result['message'] === 'Nenhuma palavra proibida encontrada') {
                                // Não salvar este resultado no banco de dados
                                continue;
                            }
    
                            SearchResult::create([
                                'marca' => $marca, // Certifique-se de que $data['marca'] está disponível
                                'link' => $result['link'],
                                'palavra_proibida' => $result['palavra_proibida'] ?? 'Nenhuma'
                            ]);
                        }
                    }
    
                    return response()->json($rpaResults);
                } else {
                    Log::error("Erro ao decodificar JSON: " . json_last_error_msg());
                    return response()->json(['error' => 'Erro ao decodificar JSON'], 500);
                }
            } else {
                Log::error("Erro ao executar o script Python: " . $errorOutput);
                return response()->json(['error' => 'Erro ao processar a pesquisa de marcas'], 500);
            }
        } else {
            Log::error("Falha ao iniciar o processo Python");
            return response()->json(['error' => 'Erro ao iniciar o processo Python'], 500);
        }
    }
    
    
    private function executeRpaForLink($link) {
        $command = escapeshellcmd("python3 scripts/runLink.py " . escapeshellarg($link));
    
        $descriptorspec = [
            0 => ["pipe", "r"],
            1 => ["pipe", "w"],
            2 => ["pipe", "w"]
        ];
    
        $process = proc_open($command, $descriptorspec, $pipes);
    
        if (is_resource($process)) {
            fclose($pipes[0]);
    
            $output = stream_get_contents($pipes[1]);
            fclose($pipes[1]);
    
            $errorOutput = stream_get_contents($pipes[2]);
            fclose($pipes[2]);
    
            $returnValue = proc_close($process);
    
            if ($returnValue === 0) {
                // Supondo que $output já seja uma string JSON válida
                $result = json_decode($output, true);
            
                Log::info("RPA Output: " . $output);
                Log::info("Result: " . print_r($result, true)); // Melhora a depuração
            
                if (json_last_error() === JSON_ERROR_NONE) {
                    return ['status' => 'success', 'data' => $result];
                } else {
                    Log::error("Erro ao decodificar JSON: " . json_last_error_msg());
                    return ['status' => 'error', 'message' => 'Erro ao decodificar JSON'];
                }
            } else {
                Log::error("Erro ao executar o script RPA: " . $errorOutput);
                return ['status' => 'error', 'message' => 'Erro ao executar o script RPA'];
            }            
        } else {
            Log::error("Falha ao iniciar o processo RPA");
            return ['status' => 'error', 'message' => 'Erro ao iniciar o processo RPA'];
        }
    }

    public function relMarcas(){
        return view('relMarcas');
    }

    public function getMarcas(){
        return SearchResult::all();
    }

    public function viewAddUser(){
        Log::info(Auth::user()->id);
        if (Auth::user()->id == '1') {
            // O usuário é admin
            return view('addUser');
        } else {
            // O usuário não é admin
            abort(403, 'Acesso negado. Você não tem permissão para acessar esta página.');
        }

    }

    public function getUsers(){
        return User::all();
    }

    public function updateOrCreateUsers(Request $request, $id = null)
    {
        Log::info($request);
        $data = $request;
        $user = User::updateOrCreate(
            ['id' => $id], // Se $id for null, irá criar um novo usuário
            ['name' => $data['name'], 'email' => $data['usuario'], 'password' => bcrypt($data['senha'])]
        );    
    
        return response()->json($user);
    }

    public function deleteUsers($id){
        $user = User::find($id);
        $user->delete();
    }
    

}
