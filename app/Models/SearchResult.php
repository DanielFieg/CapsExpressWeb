<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class SearchResult extends Model
{
    protected $table = 'resultadoPesquisa';
    public $timestamps = true;

    protected $fillable = [
        'marca',
        'link',
        'palavra_proibida',
    ];
}
