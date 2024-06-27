<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CapsExpress</title>
  <link rel="shortcut icon" type="image/png" href="" />
  <link rel="stylesheet" href="css/styles.min.css" />
  <style>
    .block-ui {
      pointer-events: none;
      user-select: none;
      opacity: 0.5;
    }
  </style>
</head>

<body>
  <!--  Body Wrapper -->
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
              <span class="hide-menu">Home</span>
            </li>
            <li class="sidebar-item">
              <a class="sidebar-link" href="{{ route('home') }}" aria-expanded="false">
                <span>
                  <i class="ti ti-layout-dashboard"></i>
                </span>
                <span class="hide-menu">Dashboard</span>
              </a>
            </li>
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
              <a class="sidebar-link"  href="{{ route('logout') }}" aria-expanded="false" >
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
      <!--  Header Start -->
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
      <!--  Header End -->
      <div class="container-fluid">
        <div class="container-fluid">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title fw-semibold mb-4">PESQUISAR MARCAS</h5>
              <div class="card">
                <div class="card-body">
                  <form id="searchForm" class="position-relative" @submit.prevent="submitSearch">
                    <button @click.prevent="openSweetAlert" type="button"
                      class="btn btn-primary position-absolute top-0 end-0 translate-middle-y ti ti-plus">
                      <i class="fa fa-search"></i>
                    </button>
                    <div class="mb-3">
                      <label for="disabledSelect" class="form-label">Selecione uma Marca</label>
                      <select id="marcaSelect" class="form-select" v-model="selectedMarca">
                        <option value="">Selecione uma Marca</option>
                        <option v-for="marca in marcas" :key="marca.id" :value="marca">@{{ marca.marca }}</option>
                      </select>
                    </div>
                    <button v-if="searchButtonVisible" type="submit" class="btn btn-primary">Pesquisar</button>
                    <p v-if="!searchButtonVisible" class="alert alert-warning">@{{ limitReachedMessage }}</p>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <!-- Tabela de Resultados -->
          <div class="card" v-if="searchResults.length || noResultsMessage">
            <div class="card-body">
              <h5 class="card-title fw-semibold mb-4">RESULTADOS</h5>
              <div v-if="noResultsMessage" class="alert alert-warning">
                @{{ noResultsMessage }}
              </div>
              <div v-else class="table-responsive">
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th>Link</th>
                      <th>Palavra Proibida</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="result in searchResults" :key="result.id">
                      <td>@{{ result.link }}</td>
                      <td>@{{ result.palavra_proibida }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <button class="btn btn-primary" @click="exportToExcel">Exportar para Excel</button>
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
  <!-- Load SheetJS -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>


  <!-- Custom Script -->
  <script>
    new Vue({
      el: '#main-wrapper',
      data: {
        marcas: [], // Array para armazenar as marcas
        selectedMarca: null, // Propriedade para armazenar a marca selecionada
        searchResults: [], // Armazena os resultados da pesquisa
        noResultsMessage: '', // Mensagem para quando não há resultados
        loadingSearch: false, // Estado para controlar o carregamento da pesquisa
        searchButtonVisible: true, // controla a visibilidade do botão "Pesquisar"
        limitReachedMessage: '', // mensagem a ser exibida quando o limite é atingido
      },
      methods: {
        openSweetAlert() {
          Swal.fire({
            title: 'Cadastro de Marca',
            text: 'Digite o nome da marca:',
            input: 'text',
            inputAttributes: {
              autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Cadastrar',
            cancelButtonText: 'Cancelar',
            showLoaderOnConfirm: true,
            preConfirm: (marca) => {
              // Enviar uma solicitação AJAX para cadastrar a marca
              return axios.post('/addmarcas', { marca })
                .then(response => {
                  if (!response.data.success) {
                    throw new Error(response.data.message || 'Erro ao cadastrar a marca');
                  }
                  return response.data.marca;
                })
                .catch(error => {
                  Swal.showValidationMessage(
                    `Erro ao cadastrar: ${error.message}`
                  );
                });
            },
            allowOutsideClick: () => !Swal.isLoading()
          }).then((result) => {
            if (result.isConfirmed) {
              Swal.fire(
                'Marca cadastrada!',
                'A marca foi cadastrada com sucesso.',
                'success'
              );
              this.listarMarcas();
            }
          });
        },
        listarMarcas() {
          axios.get('/listMarcas')
            .then(response => {
              // Verifique se a resposta tem dados válidos
              if (response.data && Array.isArray(response.data)) {
                // Atribua os dados diretamente à propriedade marcas
                this.marcas = response.data;
                console.log(this.marcas);
              } else {
                console.error('Resposta da API inválida:', response);
              }
            })
            .catch(error => {
              console.error('Erro ao obter marcas:', error);
            });
        },
        submitSearch() {
          // Verificar se uma marca foi selecionada
          if (!this.selectedMarca) {
            Swal.fire({
              title: 'Erro',
              text: 'Por favor, selecione uma marca antes de pesquisar.',
              icon: 'error',
              confirmButtonText: 'Ok'
            });
            return; // Impedir a execução da pesquisa
          }

          // Impedir ações enquanto a pesquisa está em andamento
          if (this.loadingSearch) return;

          this.loadingSearch = true; // Ativar o estado de carregamento
          this.errorLimitReached = false; // Reiniciar a variável de erro

          Swal.fire({
            title: 'Carregando...',
            text: 'Aguarde enquanto processamos sua solicitação.',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
              Swal.showLoading();
              document.body.classList.add('block-ui');
            }
          });

          axios.get('/searchMarcas', {
              params: {
                id: this.selectedMarca.id,
                marca: this.selectedMarca.marca
              }
            })
            .then(response => {
              if (response.data && Array.isArray(response.data)) {
                this.searchResults = response.data; // Atualize a tabela com os resultados da pesquisa
                this.noResultsMessage = ''; // Limpe a mensagem de não resultados
                console.log(this.searchResults);
              } else if (response.data && response.data.message) {
                // Caso a API retorne uma mensagem de "Nenhum dado encontrado"
                this.searchResults = []; // Limpe os resultados anteriores
                this.noResultsMessage = response.data.message; // Exiba a mensagem de não resultados
                console.log(response.data.message);
              } else {
                console.error('Resposta da API inválida:', response);
              }
            })
            .catch(error => {
              console.error('Erro ao obter marcas:', error);
              if (error.response && error.response.status === 429) {
                // Se o status for 429 (limite de pesquisas atingido), definir o erro
                this.limitReachedMessage = 'Você atingiu o limite de 3 pesquisas por hora. Tente novamente mais tarde.';
                this.searchButtonVisible = false; // Ocultar o botão de pesquisa
              }
            })
            .finally(() => {
              this.loadingSearch = false; // Desativar o estado de carregamento após a conclusão da pesquisa
              Swal.close(); // Fechar o SweetAlert após a conclusão
              document.body.classList.remove('block-ui');
            });
        },
        exportToExcel() {
          const worksheet = XLSX.utils.json_to_sheet(this.searchResults);
          const workbook = XLSX.utils.book_new();
          XLSX.utils.book_append_sheet(workbook, worksheet, "Results");
          XLSX.writeFile(workbook, "Resultados.xlsx");
        },
      },
      mounted() {
        this.listarMarcas();
      },
      watch: {
        loadingSearch(newValue) {
          if (newValue) {
            Swal.fire({
              title: 'Carregando...',
              text: 'Aguarde enquanto processamos sua solicitação.',
              allowOutsideClick: false,
              allowEscapeKey: false,
              didOpen: () => {
                Swal.showLoading();
                document.body.classList.add('block-ui');
              }
            });
          } else {
            Swal.close();
            document.body.classList.remove('block-ui');
          }
        }
      }
    });
  </script>

</body>

</html>
