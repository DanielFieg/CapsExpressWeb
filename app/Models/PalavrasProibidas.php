<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PalavrasProibidas extends Model
{
    protected $table = 'palavrasProibidas';
    public $timestamps = true;

    protected $fillable = [
        'palavra_proibida',
    ];
}
