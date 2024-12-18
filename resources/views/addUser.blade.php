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
      <div>
        <div class="brand-logo d-flex align-items-center justify-content-between">
          <a class="text-nowrap" style="font-weight: bold; font-size: 24px; text-align: center;">CAPSEXPRESS</a>
          <div class="close-btn d-xl-none d-block sidebartoggler cursor-pointer" id="sidebarCollapse">
            <i class="ti ti-x fs-8"></i>
          </div>
        </div>
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
      </div>
    </aside>
    <div class="body-wrapper">
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
      <div class="container-fluid">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title fw-semibold mb-4">RELATÓRIO DE USUÁRIOS</h5>
            <div class="card">
              <!-- Tabela de Resultados -->
              <div class="card" v-if="usuarios.length > 0">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center mb-4">
                    <h5 class="card-title fw-semibold">USUÁRIOS</h5>
                    <button class="btn btn-success" @click="criarUsuario">
                      <i class="ti ti-plus"></i> Usuário
                    </button>
                  </div>
                  <div class="table-responsive">
                    <table class="table table-bordered">
                      <thead>
                        <tr>
                          <th>Nome</th>
                          <th>Usuário</th>
                          <th>Ações</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="usuario in usuarios" :key="usuario.id">
                          <td>@{{ usuario.name }}</td>
                          <td>@{{ usuario.email }}</td>
                          <td>
                            <button class="btn btn-primary" @click="editarUsuario(usuario)">Editar</button>
                            <button class="btn btn-danger" @click="deletarUsuario(usuario)">Deletar</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <div v-else>
                <p>Nenhum usuário encontrado.</p>
              </div>
            </div>
          </div>
        </div>
      </div>      
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <script>
    new Vue({
      el: '#main-wrapper',
      data: {
        usuarios: [] // Armazena os usuários
      },
      mounted() {
        this.fetchUsers();
      },
      methods: {
        fetchUsers() {
          axios.get('{{ route('users.get') }}')
            .then(response => {
              this.usuarios = response.data;
              console.log(this.usuarios);
            })
            .catch(error => {
              console.error("Erro ao buscar usuários:", error);
            });
        },
        saveUser(id = null) {
          const name = document.getElementById('swal-input1').value;
          const usuario = document.getElementById('swal-input2').value;
          const senha = document.getElementById('swal-input3').value;

          if (!name || !usuario) {
            Swal.showValidationMessage('Por favor, preencha todos os campos obrigatórios');
            return;
          }

          const url = id ? `/updateOrCreateUsers/${id}` : '/updateOrCreateUsers';
          const method = 'POST';

          const data = { name, usuario };
          if (senha) {
            data.senha = senha; // Inclui nova senha apenas se fornecida
          }

          axios({ method, url, data })
            .then(response => {
              Swal.fire('Sucesso', `Usuário ${id ? 'atualizado' : 'criado'} com sucesso`, 'success');
              this.fetchUsers(); // Recarrega os usuários
            })
            .catch(error => {
              Swal.fire('Erro', `Não foi possível ${id ? 'atualizar' : 'criar'} o usuário`, 'error');
            });
        },
        editarUsuario(usuario) {
          Swal.fire({
            title: 'Editar Usuário',
            html: this.getUserFormHtml(usuario),
            focusConfirm: false,
            preConfirm: () => this.saveUser(usuario.id)
          });
        },
        criarUsuario() {
          Swal.fire({
            title: 'Adicionar Usuário',
            html: this.getUserFormHtml(),
            focusConfirm: false,
            preConfirm: () => this.saveUser()
          });
        },
        getUserFormHtml(usuario = {}) {
          return `
            <div style="display: flex; flex-direction: column; gap: 10px;">
              <div style="display: flex; align-items: center;">
                <label for="swal-input1" style="width: 80px;">Nome:</label>
                <input id="swal-input1" class="swal2-input" placeholder="Nome" value="${usuario.name || ''}" style="flex: 1;">
              </div>
              <div style="display: flex; align-items: center;">
                <label for="swal-input2" style="width: 80px;">Usuário:</label>
                <input id="swal-input2" class="swal2-input" placeholder="Usuário" value="${usuario.email || ''}" style="flex: 1;">
              </div>
              <div style="display: flex; align-items: center;">
                <label for="swal-input3" style="width: 80px;">Nova Senha:</label>
                <input id="swal-input3" class="swal2-input" type="password" placeholder="Nova Senha" style="flex: 1;">
              </div>
            </div>`;
        },
        deletarUsuario(usuario) {
          Swal.fire({
            title: 'Tem certeza?',
            text: `Você está prestes a deletar o usuário ${usuario.name}.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim, deletar!',
            cancelButtonText: 'Cancelar'
          }).then((result) => {
            if (result.isConfirmed) {
              axios.delete(`/deleteUsers/${usuario.id}`)
                .then(response => {
                  Swal.fire('Deletado!', 'Usuário deletado com sucesso.', 'success');
                  this.fetchUsers(); // Recarrega os usuários
                })
                .catch(error => {
                  Swal.fire('Erro', 'Não foi possível deletar o usuário', 'error');
                });
            }
          });
        }
      }
    });
  </script>
  
</body>

</html>
