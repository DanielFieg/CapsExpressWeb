<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Clicks extends Migration
{
    public function up()
    {
        Schema::create('click_limits', function (Blueprint $table) {
            $table->id();
            $table->string('ip_address');
            $table->integer('click_count')->default(0);
            $table->timestamp('last_clicked_at')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('click_limits');
    }
}
