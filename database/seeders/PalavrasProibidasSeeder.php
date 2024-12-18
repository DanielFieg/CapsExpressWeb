<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PalavrasProibidasSeeder extends Seeder
{
    public function run()
    {
        $palavras = [
            "Tratamento", "Garantido", "Sem riscos", "Efeito imediato",
            "Aprovação Anvisa", "100% seguro", "Resultados permanentes", "Aprovado pela FDA",
            "Clinicamente comprovado", "Milagroso", "Revolucionário", "Poderoso", "Instantâneo",
            "Sem esforço", "Todos os naturais", "Sem efeitos colaterais", "Testado em laboratório",
            "Pesquisa científica", "Fórmula exclusiva", "Detox", "Queima gordura", "Anti-idade",
            "Aumenta a imunidade", "Sem contraindicações", "Absorção completa", "Bio-disponível",
            "Sem aditivos", "Sem conservantes", "Nutricionista recomendado", "Médico aprovado",
            "Fortalece os ossos", "Melhora a memória", "Antioxidante", "Supressor de apetite",
            "Aumenta a energia", "Promove o sono", "Reduz o estresse", "Sem glúten", "Orgânico",
            "Vegan", "Aumenta a libido", "Anticancerígeno", "Anti-inflamatório", "Regula a tireoide",
            "Sem lactose", "Controla a diabetes", "Reduz o colesterol", "Promove a saúde do coração",
            "Desintoxica o fígado", "Perda de peso rápida", "Efeito lifting", "Rejuvenescedor",
            "Bloqueador de carboidratos", "Inibidor de apetite", "Remédio natural",
            "Alternativa a medicamentos", "Cura natural", "Solução definitiva",
            "Desempenho atlético superior", "Substituto de refeição", "Suplemento milagroso",
            "Resultados em dias", "Elimina toxinas", "Sem necessidade de exercício",
            "Aumenta a massa muscular", "Sem necessidade de dieta", "Resultados para toda a vida",
            "Aprovação científica", "Reduz sintomas de", "Impulsionador de energia",
            "Redução de estresse instantânea", "Alívio da dor natural", "Melhor que",
            "Alternativa segura a cirurgias", "Reduz a pressão arterial", "Controla a ansiedade",
            "Combate a depressão", "Impede o envelhecimento", "Previne doenças crônicas",
            "Promove a saúde cerebral", "Fortalece o sistema imunológico",
            "Reduz o risco de doenças cardíacas", "Controle de açúcar no sangue",
            "Livre de efeitos colaterais negativos", "Pílula da beleza", "Solução antienvelhecimento",
            "Efeito detox poderoso", "Reduz a fadiga", "Estimulante metabólico",
            "Promove a saúde da pele", "Cápsula de bem-estar", "Melhora a saúde digestiva",
            "Solução para insônia", "Reforço imunológico", "Potencializa a função cerebral",
            "Supressor de fome", "Acelerador de metabolismo", "Elixir da juventude",
            "Cápsula energética"
        ];

        foreach ($palavras as $palavra) {
            DB::table('palavrasProibidas')->insert([
                'palavra_proibida' => $palavra,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
