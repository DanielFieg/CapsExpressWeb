<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LoginController;
use App\Http\Controllers\AdminController;

// Rotas públicas acessíveis sem autenticação
Route::get('/', [LoginController::class, 'loginView'])->name('login');
Route::post('/auth', [LoginController::class, 'auth'])->name('auth.user');

Route::middleware(['auth'])->group(function () {
    // Rotas protegidas pelo middleware de autenticação
    Route::get('/apiMarcas', [AdminController::class, 'viewMarcas'])->name('form.marcas');
    Route::post('/addmarcas', [AdminController::class, 'createMarcas'])->name('create.marcas');
    Route::get('/listMarcas', [AdminController::class, 'listMarcas'])->name('list.marcas');
    Route::get('/logout', [LoginController::class, 'logout'])->name('logout');
    Route::get('/searchMarcas', [AdminController::class, 'searchMarcas'])->name('search.marcas');
    Route::get('/relatorio', [AdminController::class, 'relMarcas'])->name('rel.marcas');
    Route::get('/getMarcas', [AdminController::class, 'getMarcas'])->name('get.marcas');
    Route::get('/viewUser', [AdminController::class, 'viewAddUser'])->name('view.addUser');
    Route::get('/getUsers', [AdminController::class, 'getUsers'])->name('users.get');
    Route::post('/updateOrCreateUsers/{id?}', [AdminController::class, 'updateOrCreateUsers'])->name('updateOrCreate.post');
    Route::delete('/deleteUsers/{id}', [AdminController::class, 'deleteUsers'])->name('delete.post');
});
