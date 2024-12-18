<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('palavrasProibidas', function (Blueprint $table) {
            $table->id();
            $table->string('palavra_proibida');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('palavrasProibidas');
    }
};