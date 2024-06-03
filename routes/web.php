<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LoginController;

Route::get('/', [LoginController::class, 'loginView'])->name('loginView');
Route::post('/auth', [LoginController::class, 'auth'])->name('auth.user');