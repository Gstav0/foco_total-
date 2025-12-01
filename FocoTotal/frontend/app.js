// app.js

document.addEventListener('DOMContentLoaded', () => {
    
    const API_URL = '';

    // --- Estado ---
    let token = localStorage.getItem('token');
    let materiaSelecionadaId = null;

    // --- Elementos de Autenticação ---
    const authContainer = document.getElementById('auth-container');
    const appContainer = document.getElementById('app-container');
    const userInfo = document.getElementById('user-info');
    const usernameDisplay = document.getElementById('username-display');
    const btnLogout = document.getElementById('btn-logout');

    // Sliding Auth Elements
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const containerLogin = document.getElementById('container-login');

    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');

    // --- Elementos da Aplicação ---
    const formNovaMateria = document.getElementById('form-nova-materia');
    const inputNomeMateria = document.getElementById('nome-materia');
    const inputNomeProfessor = document.getElementById('nome-professor');
    const listaMateriasContainer = document.getElementById('lista-materias');

    const detalheNomeMateria = document.getElementById('detalhe-nome-materia');
    const detalheNomeProfessor = document.getElementById('detalhe-nome-professor');
    const btnApagarMateria = document.getElementById('btn-apagar-materia');

    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Resumo
    const tempoTotalEl = document.getElementById('tempo-total');
    const pontosFocoEl = document.getElementById('pontos-foco');
    const listaSessoesEl = document.getElementById('lista-sessoes');
    const formNovaSessao = document.getElementById('form-nova-sessao');
    const inputDuracao = document.getElementById('duracao-minutos');
    const inputDataSessao = document.getElementById('data-sessao');
    const inputDescricaoSessao = document.getElementById('descricao-sessao');

    // Tarefas
    const listaTarefasEl = document.getElementById('lista-tarefas');
    const formNovaTarefa = document.getElementById('form-nova-tarefa');
    const inputDescricaoTarefa = document.getElementById('descricao-tarefa');

    // Metas
    const listaMetasEl = document.getElementById('lista-metas');
    const formNovaMeta = document.getElementById('form-nova-meta');
    const inputHorasAlvo = document.getElementById('horas-alvo');
    const selectPeriodoMeta = document.getElementById('periodo-meta');

    // Anotações
    const listaAnotacoesEl = document.getElementById('lista-anotacoes');
    const formNovaAnotacao = document.getElementById('form-nova-anotacao');
    const inputConteudoAnotacao = document.getElementById('conteudo-anotacao');

    // Recursos
    const listaRecursosEl = document.getElementById('lista-recursos');
    const formNovoRecurso = document.getElementById('form-novo-recurso');
    const inputTituloRecurso = document.getElementById('titulo-recurso');
    const inputLinkRecurso = document.getElementById('link-recurso');


    // --- Funções Auxiliares ---

    function getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    }

    function checkAuth() {
        if (token) {
            authContainer.style.display = 'none';
            appContainer.style.display = 'flex';
            userInfo.style.display = 'flex';
            fetchUserInfo();
            fetchMaterias();
        } else {
            authContainer.style.display = 'flex';
            appContainer.style.display = 'none';
            userInfo.style.display = 'none';
        }
    }

    async function fetchUserInfo() {
        /*
        if (token === 'demo-token') {
            usernameDisplay.textContent = `Olá, Administrador`;
            return;
        }
        */

        try {
            const resp = await fetch(`${API_URL}/auth/users/me`, { headers: getHeaders() });
            if (resp.ok) {
                const user = await resp.json();
                usernameDisplay.textContent = `Olá, ${user.username}`;
            } else {
                logout();
            }
        } catch (e) {
            logout();
        }
    }

    function logout() {
        localStorage.removeItem('token');
        token = null;
        checkAuth();
    }

    // --- Autenticação ---

    if (signUpButton && signInButton && containerLogin) {
        signUpButton.addEventListener('click', () => {
            containerLogin.classList.add("right-panel-active");
        });

        signInButton.addEventListener('click', () => {
            containerLogin.classList.remove("right-panel-active");
        });
    }

    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value.trim();

        // MODO DEMO / ADMIN - REMOVIDO PARA USAR BACKEND REAL
        /*
        if (username === 'admin' && password === 'admin') {
            token = 'demo-token';
            localStorage.setItem('token', token);
            checkAuth();
            return;
        }
        */

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const resp = await fetch(`${API_URL}/auth/token`, {
                method: 'POST',
                body: formData
            });

            if (resp.ok) {
                const data = await resp.json();
                token = data.access_token;
                localStorage.setItem('token', token);
                checkAuth();
            } else {
                alert('Login falhou. Verifique suas credenciais.');
            }
        } catch (e) {
            console.error(e);
            alert('Erro ao conectar com o servidor.');
        }
    });

    formRegister.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('register-username').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value.trim();

        try {
            const resp = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            if (resp.ok) {
                alert('Conta criada com sucesso! Faça login.');
                signInButton.click(); // Switch to login view
            } else {
                const err = await resp.json();
                alert(`Erro ao registrar: ${err.detail}`);
            }
        } catch (e) {
            console.error(e);
            alert('Erro ao registrar.');
        }
    });

    btnLogout.addEventListener('click', logout);


    // --- Tabs Logic ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active to clicked
            btn.classList.add('active');
            const tabId = btn.dataset.tab;
            document.getElementById(tabId).classList.add('active');
        });
    });


    // --- Matérias ---

    async function fetchMaterias() {
        /*
        if (token === 'demo-token') {
            renderMaterias([
                { id: 1, nome_materia: 'Design de Interfaces', nome_professor: 'Prof. Gustavo' },
                { id: 2, nome_materia: 'Desenvolvimento Web', nome_professor: 'Prof. Silva' },
                { id: 3, nome_materia: 'Gestão de Projetos', nome_professor: 'Prof. Mendes' }
            ]);
            return;
        }
        */

        try {
            const response = await fetch(`${API_URL}/materias/`, { headers: getHeaders() });
            if (!response.ok) throw new Error('Erro ao buscar matérias');
            const materias = await response.json();
            renderMaterias(materias);
        } catch (error) {
            console.error(error);
            listaMateriasContainer.innerHTML = '<p>Erro ao carregar matérias.</p>';
        }
    }

    function renderMaterias(materias) {
        listaMateriasContainer.innerHTML = '';
        if (materias.length === 0) {
            listaMateriasContainer.innerHTML = '<p>Nenhuma matéria encontrada.</p>';
            return;
        }

        materias.forEach(materia => {
            const div = document.createElement('div');
            div.classList.add('materia-item');
            div.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                    <div>
                        <h4>${materia.nome_materia}</h4>
                        <p>${materia.nome_professor || ''}</p>
                    </div>
                    <span style="font-size: 0.85rem; color: var(--text-secondary); white-space: nowrap;">
                        ${materia.tempo_total || 0} min
                    </span>
                </div>
            `;
            
            div.addEventListener('click', () => {
                // Remove active de todos
                document.querySelectorAll('.materia-item').forEach(item => item.classList.remove('active'));
                // Adiciona active ao atual
                div.classList.add('active');
                selectMateria(materia);
            });
            
            listaMateriasContainer.appendChild(div);
        });
    }

    formNovaMateria.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const resp = await fetch(`${API_URL}/materias/`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    nome_materia: inputNomeMateria.value,
                    nome_professor: inputNomeProfessor.value || null
                })
            });
            if (resp.ok) {
                inputNomeMateria.value = '';
                inputNomeProfessor.value = '';
                fetchMaterias();
            }
        } catch (e) { console.error(e); }
    });

    function selectMateria(materia) {
        materiaSelecionadaId = materia.id;
        detalheNomeMateria.textContent = materia.nome_materia;
        detalheNomeProfessor.textContent = materia.nome_professor || '';
        btnApagarMateria.disabled = false;

        // Limpar dados anteriores
        tempoTotalEl.textContent = 'Carregando...';
        pontosFocoEl.textContent = '...';
        listaSessoesEl.innerHTML = '<li>Carregando...</li>';
        listaTarefasEl.innerHTML = '<li>Carregando...</li>';
        listaMetasEl.innerHTML = '<li>Carregando...</li>';
        listaAnotacoesEl.innerHTML = '<p>Carregando...</p>';
        listaRecursosEl.innerHTML = '<li>Carregando...</li>';

        // Load all data for this subject
        fetchSumario(materia.id);
        fetchTarefas(materia.id);
        fetchMetas(materia.id);
        fetchAnotacoes(materia.id);
        fetchRecursos(materia.id);
    }

    btnApagarMateria.addEventListener('click', async () => {
        if (!materiaSelecionadaId || !confirm('Tem certeza?')) return;
        try {
            await fetch(`${API_URL}/materias/${materiaSelecionadaId}`, { method: 'DELETE', headers: getHeaders() });
            materiaSelecionadaId = null;
            detalheNomeMateria.textContent = 'Selecione uma matéria';
            btnApagarMateria.disabled = true;
            fetchMaterias();
        } catch (e) { console.error(e); }
    });


    // --- Sessões (Resumo) ---

    async function fetchSumario(id) {
        /*
        if (token === 'demo-token') {
            tempoTotalEl.textContent = `120 minutos`;
            pontosFocoEl.textContent = `Score: 850`;
            listaSessoesEl.innerHTML = `<li>45 min - ${new Date().toLocaleDateString()}</li><li>30 min - ${new Date().toLocaleDateString()}</li>`;
            return;
        }
        */

        const resp = await fetch(`${API_URL}/sessoes/materias/${id}/sumario`, { headers: getHeaders() });
        if (resp.ok) {
            const data = await resp.json();
            tempoTotalEl.textContent = `${data.total_minutos} minutos`;
            pontosFocoEl.textContent = `Score: ${data.total_pontos_foco}`;
            listaSessoesEl.innerHTML = data.sessoes.map(s => 
                `<li>${s.duracao_minutos} min - ${new Date(s.data_sessao).toLocaleDateString()}</li>`
            ).join('') || '<li>Nenhuma sessão.</li>';
        }
    }

    formNovaSessao.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!materiaSelecionadaId) {
            alert("Selecione uma matéria primeiro!");
            return;
        }
        
        try {
            const resp = await fetch(`${API_URL}/sessoes/materias/${materiaSelecionadaId}/sessoes`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({
                    duracao_minutos: parseInt(inputDuracao.value),
                    data_sessao: inputDataSessao.value || null,
                    descricao: inputDescricaoSessao.value
                })
            });

            if (resp.ok) {
                inputDuracao.value = '';
                inputDescricaoSessao.value = '';
                inputDataSessao.value = '';
                fetchSumario(materiaSelecionadaId);
                fetchMaterias(); // Atualiza lista lateral com novo tempo
            } else {
                const err = await resp.json();
                alert(`Erro ao registrar sessão: ${err.detail}`);
            }
        } catch (e) {
            console.error(e);
            alert('Erro ao conectar com o servidor.');
        }
    });


    // --- Tarefas ---

    async function fetchTarefas(id) {
        const resp = await fetch(`${API_URL}/tarefas/?materia_id=${id}`, { headers: getHeaders() });
        if (resp.ok) {
            const tarefas = await resp.json();
            listaTarefasEl.innerHTML = '';
            if (tarefas.length === 0) listaTarefasEl.innerHTML = '<li>Nenhuma tarefa.</li>';
            
            tarefas.forEach(t => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <input type="checkbox" class="task-checkbox" ${t.concluida ? 'checked' : ''}>
                    <span class="${t.concluida ? 'task-done' : ''}">${t.descricao}</span>
                `;
                const checkbox = li.querySelector('.task-checkbox');
                checkbox.addEventListener('change', () => toggleTarefa(t, checkbox.checked));
                listaTarefasEl.appendChild(li);
            });
        }
    }

    async function toggleTarefa(tarefa, checked) {
        await fetch(`${API_URL}/tarefas/${tarefa.id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify({ descricao: tarefa.descricao, concluida: checked })
        });
        fetchTarefas(materiaSelecionadaId);
    }

    formNovaTarefa.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!materiaSelecionadaId) {
            alert("Selecione uma matéria primeiro!");
            return;
        }

        try {
            const resp = await fetch(`${API_URL}/tarefas/?materia_id=${materiaSelecionadaId}`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({ descricao: inputDescricaoTarefa.value, concluida: false })
            });

            if (resp.ok) {
                inputDescricaoTarefa.value = '';
                fetchTarefas(materiaSelecionadaId);
            } else {
                const err = await resp.json();
                alert(`Erro ao criar tarefa: ${err.detail}`);
            }
        } catch (e) {
            console.error(e);
            alert('Erro ao conectar com o servidor.');
        }
    });


    // --- Metas ---

    async function fetchMetas(id) {
        const resp = await fetch(`${API_URL}/metas/?materia_id=${id}`, { headers: getHeaders() });
        if (resp.ok) {
            const metas = await resp.json();
            listaMetasEl.innerHTML = metas.map(m => 
                `<li>${m.horas_alvo} horas (${m.periodo})</li>`
            ).join('') || '<li>Nenhuma meta.</li>';
        }
    }

    formNovaMeta.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!materiaSelecionadaId) return;
        await fetch(`${API_URL}/metas/?materia_id=${materiaSelecionadaId}`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ horas_alvo: inputHorasAlvo.value, periodo: selectPeriodoMeta.value })
        });
        inputHorasAlvo.value = '';
        fetchMetas(materiaSelecionadaId);
    });


    // --- Anotações ---

    async function fetchAnotacoes(id) {
        const resp = await fetch(`${API_URL}/anotacoes/?materia_id=${id}`, { headers: getHeaders() });
        if (resp.ok) {
            const notas = await resp.json();
            listaAnotacoesEl.innerHTML = notas.map(n => `
                <div class="note-card">
                    <p>${n.conteudo}</p>
                    <span class="note-date">${new Date(n.data_criacao).toLocaleDateString()}</span>
                </div>
            `).join('');
        }
    }

    formNovaAnotacao.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!materiaSelecionadaId) return;
        await fetch(`${API_URL}/anotacoes/?materia_id=${materiaSelecionadaId}`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ conteudo: inputConteudoAnotacao.value })
        });
        inputConteudoAnotacao.value = '';
        fetchAnotacoes(materiaSelecionadaId);
    });


    // --- Recursos ---

    async function fetchRecursos(id) {
        const resp = await fetch(`${API_URL}/recursos/materias/${id}/recursos`, { headers: getHeaders() });
        if (resp.ok) {
            const recursos = await resp.json();
            listaRecursosEl.innerHTML = recursos.map(r => 
                `<li><a href="${r.link_url}" target="_blank">${r.titulo}</a></li>`
            ).join('') || '<li>Nenhum recurso.</li>';
        }
    }

    formNovoRecurso.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!materiaSelecionadaId) return;
        await fetch(`${API_URL}/recursos/materias/${materiaSelecionadaId}/recursos`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ titulo: inputTituloRecurso.value, link_url: inputLinkRecurso.value })
        });
        inputTituloRecurso.value = '';
        inputLinkRecurso.value = '';
        fetchRecursos(materiaSelecionadaId);
    });


    // --- Inicialização ---
    
    // Forçar logout se for token antigo de demo
    if (token === 'demo-token') {
        logout();
    } else {
        checkAuth();
    }

});
