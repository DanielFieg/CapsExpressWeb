<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Clicks extends Model
{
    protected $table = 'click_limits';
    public $timestamps = true;

    protected $fillable = [
        'ip_address',
        'click_count',
        'last_clicked_at',
    ];

    protected $casts = [
        'last_clicked_at' => 'datetime',
    ];
}
