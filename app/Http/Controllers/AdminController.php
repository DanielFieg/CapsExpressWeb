<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Marcas;
use Symfony\Component\HttpFoundation\Request;
use Illuminate\Support\Facades\Log;
use App\Models\SearchResult;

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

    public function searchMarcas(Request $request) {
        set_time_limit(300);
    
        $id = $request->query('id');
        $marca = $request->query('marca');
        Log::info($id);
        Log::info($marca);
    
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
                Log::info("Output :" . $output);
    
                $jsonData = json_decode($output, true);
    
                // Verifica se jsonData é um array e não está vazio
                if (is_array($jsonData) && !empty($jsonData)) {
                    foreach ($jsonData as $data) {
                        // Verifica se cada item no array é um array associativo
                        if (is_array($data) && isset($data['Marca'], $data['Link'], $data['Palavra Proibida'])) {
                            SearchResult::create([
                                'marca' => $data['Marca'],
                                'link' => $data['Link'],
                                'palavra_proibida' => $data['Palavra Proibida'],
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

}
