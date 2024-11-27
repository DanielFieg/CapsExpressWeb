<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Log;

class LoginController extends Controller{
    public function loginView(){
        return view('login');
    }

    public function auth(Request $request) {
        Log::info($request);
        $usuario = $request->input('email');
        $senha = $request->input('password');
    
        $this->validate($request,[
            'email' => 'required',
            'password' => 'required'
        ]);
    
        if (Auth::attempt(['email' => $usuario, 'password' => $senha])) {
            $user = Auth::user();
            return response()->json([
                'success' => true,
                'redirectUrl' => route('form.marcas')
            ]);
        } else {
            return response()->json([
                'success' => false
            ]);
        }
    }

    public function register(Request $request)
    {

        // Crie um novo usuário com os dados fornecidos
        $user = new User;
        $user->name = $request->input('email');
        $user->email = $request->input('email');
        $user->password = bcrypt($request->input('password')); // Use bcrypt para hash da senha

        // Salve o novo usuário no banco de dados
        $user->save();

        // Se o usuário foi criado com sucesso, você pode retornar uma resposta adequada
        return response()->json([
            'success' => true,
            'message' => 'Usuário criado com sucesso!',
        ]);
    }

    public function logout() {
        Auth::logout();
        session()->flush(); // Limpa todos os dados da sessão
    
        return redirect('/')->with('message', 'Logout realizado com sucesso.');
    }
    
    
}
