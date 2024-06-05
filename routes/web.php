<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LoginController;
use App\Http\Controllers\AdminController;

Route::get('/', [LoginController::class, 'loginView'])->name('loginView');
Route::post('/auth', [LoginController::class, 'auth'])->name('auth.user');
Route::get('/home', [AdminController::class, 'home'])->name('home');
Route::get('/apiMarcas', [AdminController::class, 'viewMarcas'])->name('form.marcas');