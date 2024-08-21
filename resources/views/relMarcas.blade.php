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
                    <a class="sidebar-link" href="{{ route('rel.marcas') }}" aria-expanded="false">
                        <span>
                        <i class="ti ti-article"></i>
                        </span>
                        <span class="hide-menu">Relatório</span>
                    </a>
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
                            <h5 class="card-title fw-semibold mb-4">RELATÓRIO DE PESQUISAS</h5>
                            <div class="card">
                                <!-- Tabela de Resultados -->
                                <div class="card" v-if="resultado.length > 0">
                                    <div class="card-body">
                                        <h5 class="card-title fw-semibold mb-4">RESULTADOS</h5>
                                        <div class="table-responsive">
                                            <table class="table table-bordered">
                                                <thead>
                                                    <tr>
                                                        <th>Marca</th>
                                                        <th>Link</th>
                                                        <th>Palavra Proibida</th>
                                                        <th>Data</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="result in resultado" :key="result.id">
                                                        <td>@{{ result.marca }}</td>
                                                        <td><a :href="result.link" target="_blank">@{{ result.link }}</a></td>
                                                        <td>@{{ result.palavra_proibida }}</td>
                                                        <td>@{{ formatarDataEHora(result.created_at) }}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                                <div class="alert alert-warning" v-if="resultado.length === 0">
                                    Nenhum resultado encontrado.
                                </div>
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
<script>
    new Vue({
        el: '#relMarcas',
        data: {
            resultado: [], // Array para armazenar os resultados
        },
        methods: {
            listarConsultas() {
                axios.get('/getMarcas')
                .then(response => {
                    // Verifique se a resposta tem dados válidos
                    if (response.data && Array.isArray(response.data)) {
                        // Atribua os dados diretamente à propriedade resultado
                        this.resultado = response.data;
                        console.log(this.resultado);
                    } else {
                        console.error('Resposta da API inválida:', response);
                    }
                })
                .catch(error => {
                    console.error('Erro ao obter marcas:', error);
                });
            },
            formatarDataEHora(data) {
                if (!data) return ''; // Retorna uma string vazia se data for nulo ou indefinido

                const dataObj = new Date(data);
                if (isNaN(dataObj.getTime())) {
                    return ''; // Retorna uma string vazia se a data não for válida
                }

                const dia = dataObj.getDate().toString().padStart(2, '0');
                const mes = (dataObj.getMonth() + 1).toString().padStart(2, '0');
                const ano = dataObj.getFullYear();
                const hora = dataObj.getHours().toString().padStart(2, '0');
                const minuto = dataObj.getMinutes().toString().padStart(2, '0');
                const segundo = dataObj.getSeconds().toString().padStart(2, '0');

                return `${dia}/${mes}/${ano} ${hora}:${minuto}:${segundo}`;
            },
        },
        created() {
            this.listarConsultas(); // Chama listarConsultas ao criar a instância Vue
        }
    });
  </script>