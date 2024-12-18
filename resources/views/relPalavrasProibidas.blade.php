<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CapsExpress</title>
  <link rel="shortcut icon" type="image/png" href="" />
  <link rel="stylesheet" href="css/styles.min.css" />
</head>

<style>
  .block-ui {
    pointer-events: none;
    user-select: none;
    opacity: 0.5;
  }
</style>

<body>
    <!-- Body Wrapper -->
    <div id="relMarcas">
        <div class="page-wrapper" id="main-wrapper" data-layout="vertical" data-navbarbg="skin6" data-sidebartype="full"
            data-sidebar-position="fixed" data-header-position="fixed">
            <!-- Sidebar Start -->
            <aside class="left-sidebar">
            <!-- Sidebar scroll-->
            <div>
                <div class="brand-logo d-flex align-items-center justify-content-between">
                <a class="text-nowrap" style="font-weight: bold; font-size: 24px; text-align: center;">CAPSEXPRESS</a>
                <div class="close-btn d-xl-none d-block sidebartoggler cursor-pointer" id="sidebarCollapse">
                    <i class="ti ti-x fs-8"></i>
                </div>
                </div>

                <!-- Sidebar navigation-->
                <nav class="sidebar-nav scroll-sidebar" data-simplebar="">
                <ul id="sidebarnav">
                    <li class="nav-small-cap">
                    <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                    <span class="hide-menu">API PESQUISA</span>
                    </li>
                    <li class="sidebar-item">
                        <a class="sidebar-link" href="{{ route('form.marcas') }}" aria-expanded="false">
                            <span>
                            <i class="ti ti-file-description"></i>
                            </span>
                            <span class="hide-menu">Pesquisar Marcas</span>
                        </a>
                    </li>
                    <li class="sidebar-item">
                        <a class="sidebar-link" href="{{ route('form.palavrasProib') }}" aria-expanded="false">
                          <span>
                            <i class="ti ti-lock"></i>
                          </span>
                          <span class="hide-menu">Palavras Proibidas</span>
                        </a>
                      </li>
                    <li class="sidebar-item">
                        <a class="sidebar-link" href="{{ route('rel.marcas') }}" aria-expanded="false">
                            <span>
                            <i class="ti ti-article"></i>
                            </span>
                            <span class="hide-menu">Relatório</span>
                        </a>
                    </li>
                    <li class="sidebar-item">
                        @if (Auth::check() && Auth::user()->id == 1) <!-- Verifica se o usuário está autenticado e o id é 6 -->
                            <a class="sidebar-link" href="{{ route('view.addUser') }}" aria-expanded="false">
                                <span>
                                    <i class="ti ti-user-plus"></i> <!-- Ícone de adicionar usuário -->
                                </span>
                                <span class="hide-menu">Cadastro de Usuários</span>
                            </a>
                        @endif
                    </li>                    
                    <li class="nav-small-cap">
                        <i class="ti ti-dots nav-small-cap-icon fs-4"></i>
                        <span class="hide-menu">AUTH</span>
                    </li>
                    <li class="sidebar-item">
                        <a class="sidebar-link" href="{{ route('logout') }}" aria-expanded="false">
                            <span>
                            <i class="ti ti-login"></i>
                            </span>
                            <span class="hide-menu">Login</span>
                        </a>
                    </li>
                </ul>
                </nav>
                <!-- End Sidebar navigation -->
            </div>
            <!-- End Sidebar scroll-->
            </aside>
            <div class="body-wrapper">
            <!-- Header Start -->
            <header class="app-header">
                <nav class="navbar navbar-expand-lg navbar-light">
                <ul class="navbar-nav">
                    <li class="nav-item d-block d-xl-none">
                    <a class="nav-link sidebartoggler nav-icon-hover" id="headerCollapse" href="javascript:void(0)">
                        <i class="ti ti-menu-2"></i>
                    </a>
                    </li>
                </ul>
                </nav>
            </header>
            <!-- Header End -->
            <div class="container-fluid">
                <div class="container-fluid">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title fw-semibold mb-4 d-flex justify-content-between align-items-center">
                                <span>PALAVRAS PROIBIDAS</span>
                                <button @click.prevent="openNewPalavra" type="button" class="btn btn-primary ti ti-plus">
                                    <i class="fa fa-search"></i>
                                </button>
                            </h5>
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Palavras Proibidas</th>
                                            <th>Excluir</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="result in resultado" :key="result.id">
                                            <td>@{{ result.id }}</td>
                                            <td>@{{ result.palavra_proibida }}</td>
                                            <td>
                                                <button @click="deletePalavra(result.id)" class="btn btn-danger btn-sm" style="margin-left: 10px;">
                                                    <i class="ti ti-trash"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>                                        
                            </div>
                        </div>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="libs/jquery/dist/jquery.min.js"></script>
<script src="libs/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="js/sidebarmenu.js"></script>
<script src="js/app.min.js"></script>
<!-- Load Vue.js -->
<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<!-- Load SweetAlert2 -->
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    

</body>

</html>
<script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>
<script>
    new Vue({
        el: '#relMarcas',
        data: {
            resultado: [], // Array para armazenar os resultados
        },
        methods: {
            listarPalavrasProibidas() {
                axios.get('/listPalavras')
                .then(response => {
                    console.log(response);
                    if (response.data && Array.isArray(response.data)) {
                        // Ordena os dados pelo ID em ordem crescente
                        this.resultado = response.data.sort((a, b) => {
                            return a.id - b.id; // Ordena por ID de forma crescente
                        });
                    } else {
                        console.error('Resposta da API inválida:', response);
                    }
                })
                .catch(error => {
                    console.error('Erro ao obter marcas:', error);
                });
            },
            openNewPalavra() {
                Swal.fire({
                    title: 'Cadastro de Palavra Proibida',
                    text: 'Digite o nome da palavra proibida:',
                    input: 'text',
                    inputAttributes: {
                        autocapitalize: 'off'
                    },
                    showCancelButton: true,
                    confirmButtonText: 'Cadastrar',
                    cancelButtonText: 'Cancelar',
                    showLoaderOnConfirm: true,
                    preConfirm: (palavra_proibida) => {
                        if (!palavra_proibida || palavra_proibida.trim() === '') {
                            Swal.showValidationMessage('Por favor, insira uma palavra proibida');
                            return false;
                        }

                        return axios.post('/addpalavra', { palavra: palavra_proibida })
                            .then(response => {
 
                            })
                            .catch(error => {
                                // Verifica se o erro é devido à palavra já cadastrada
                                console.log(error.response.data.message);
                                if (error.response.data.message) {
                                    Swal.showValidationMessage('Palavra já cadastrada.');
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Erro',
                                        text: 'Ocorreu um erro desconhecido ao cadastrar a palavra.'
                                    });
                                }
                            });
                    },
                    allowOutsideClick: () => !Swal.isLoading()
                }).then((result) => {
                    if (result.isConfirmed) {
                        Swal.fire(
                            'Palavra Proibida cadastrada!',
                            'A palavra foi cadastrada com sucesso.',
                            'success'
                        );
                        this.listarPalavrasProibidas();
                    }
                });
            },
            deletePalavra(id) {
                Swal.fire({
                    title: 'Tem certeza?',
                    text: 'Você está prestes a deletar esta palavra proibida.',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Sim, deletar!',
                    cancelButtonText: 'Cancelar',
                }).then((result) => {
                    if (result.isConfirmed) {
                        axios.delete(`/deletePalavra/${id}`)
                            .then(response => {
                                Swal.fire(
                                    'Deletado!',
                                    'A palavra proibida foi deletada com sucesso.',
                                    'success'
                                );
                                this.listarPalavrasProibidas(); // Atualiza a lista de palavras proibidas
                            })
                            .catch(error => {
                                Swal.fire(
                                    'Erro',
                                    'Não foi possível deletar a palavra proibida.',
                                    'error'
                                );
                            });
                    }
                });
            }
        },
        created() {
            this.listarPalavrasProibidas(); // Chama listarConsultas ao criar a instância Vue
        }
    });
  </script>