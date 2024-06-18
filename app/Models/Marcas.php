<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Marcas extends Model
{
    protected $table = 'marcas';
    public $timestamps = false;

    protected $fillable = [
        'marca',
    ];
}
