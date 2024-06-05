<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;

class AdminController extends Controller{
    public function home(){
        return view('home');
    }

    public function viewMarcas(){
        return view('formMarcas');
    }

}
