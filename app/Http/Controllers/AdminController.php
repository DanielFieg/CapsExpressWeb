<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Marcas;
use Symfony\Component\HttpFoundation\Request;
use Illuminate\Support\Facades\Log;
use App\Models\SearchResult;
use App\Models\Clicks;

class AdminController extends Controller
{
    public function home()
    {
        return view('home');
    }

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

    public function listMarcas(){
        $marcas = Marcas::all();
        return $marcas;
    }

    public function searchMarcas(Request $request)
    {
        set_time_limit(300);

        $ip = $request->ip(); // Obter o endereço IP do usuário
        $limit = 3; // Limite máximo de cliques por hora

        // Buscar o registro de limite de cliques pelo endereço IP
        $clickLimit = Clicks::where('ip_address', $ip)->first();

        // Verificar se o registro existe e se o número de cliques está dentro do limite
        if ($clickLimit) {
            // Verificar se o último clique foi há mais de uma hora
            $lastClickedAt = $clickLimit->last_clicked_at;
            if ($lastClickedAt && $lastClickedAt->diffInHours(now()) >= 1) {
                // Reiniciar contagem se passou mais de uma hora desde o último clique
                $clickLimit->click_count = 0;
            }

            // Verificar se o número de cliques não excedeu o limite
            if ($clickLimit->click_count >= $limit) {
                return response()->json(['error' => 'Você atingiu o limite de pesquisas por hora.'], 429);
            }
        } else {
            // Criar um novo registro se não existir um para este IP
            $clickLimit = new Clicks();
            $clickLimit->ip_address = $ip;
        }

        // Incrementar o contador de cliques e salvar
        $clickLimit->click_count++;
        $clickLimit->last_clicked_at = now();
        $clickLimit->save();

        // Continuar com a execução do script Python
        $id = $request->query('id');
        $marca = $request->query('marca');
        Log::info("ID: " . $id);
        Log::info("Marca: " . $marca);

        $command = "python scripts/rpa.py " . escapeshellarg($marca);
        $descriptorspec = [
            0 => ["pipe", "r"],
            1 => ["pipe", "w"],
            2 => ["pipe", "w"]
        ];

        $process = proc_open($command, $descriptorspec, $pipes, null, null);

        if (is_resource($process)) {
            fclose($pipes[0]);

            $output = stream_get_contents($pipes[1]);
            $errorOutput = stream_get_contents($pipes[2]);

            fclose($pipes[1]);
            fclose($pipes[2]);

            $return_value = proc_close($process);

            if ($return_value === 0) {
                Log::info("Output: " . $output);

                $jsonData = json_decode($output, true);

                if (is_array($jsonData) && !empty($jsonData)) {
                    foreach ($jsonData as $data) {
                        if (is_array($data) && isset($data['marca'], $data['link'], $data['palavra_proibida'])) {
                            SearchResult::create([
                                'marca' => $data['marca'],
                                'link' => $data['link'],
                                'palavra_proibida' => $data['palavra_proibida'],
                            ]);
                        }
                    }
                } else {
                    Log::info("Nenhum dado encontrado para a marca especificada");
                }

                return response()->json($jsonData);
            } else {
                Log::error('Erro na execução do script Python: ' . $errorOutput);
                return response()->json(['error' => 'Erro na execução do script Python: ' . $errorOutput], 500);
            }
        } else {
            Log::error('Não foi possível iniciar o processo para executar o script Python');
            return response()->json(['error' => 'Não foi possível iniciar o processo para executar o script Python'], 500);
        }
    }


    public function relMarcas(){
        return view('relMarcas');
    }

    public function getMarcas(){
        return SearchResult::all();
    }

}
