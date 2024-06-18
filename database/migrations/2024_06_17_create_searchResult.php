<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('resultadoPesquisa', function (Blueprint $table) {
            $table->id();
            $table->string('marca');
            $table->string('link');
            $table->string('palavra_proibida');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('resultadoPesquisa');
    }
};
