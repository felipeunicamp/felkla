import streamlit as st
from datetime import date, datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


def gerar_pdf_relatorio(relatorio_texto, nome_arquivo):
    """Gera um PDF a partir do texto do relatório"""
    buffer = io.BytesIO()

    # Configurar documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#006837')
    )

    # Estilo para seções
    secao_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.HexColor('#006837')
    )

    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_LEFT
    )

    # Construir conteúdo
    story = []

    # Processar o texto linha por linha
    linhas = relatorio_texto.split('\n')

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            story.append(Spacer(1, 6))
            continue

        if linha.startswith('RELATÓRIO DE AVALIAÇÃO'):
            story.append(Paragraph(linha, titulo_style))
        elif linha.startswith('====='):
            continue
        elif linha.endswith(':') and linha.isupper():
            story.append(Paragraph(f"<b>{linha}</b>", secao_style))
        elif linha.startswith('- '):
            story.append(Paragraph(linha, normal_style))
        else:
            story.append(Paragraph(linha, normal_style))

    # Adicionar rodapé
    story.append(Spacer(1, 20))
    rodape_style = ParagraphStyle(
        'Rodape',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("Relatório gerado pela Metodologia FELKLA - Klabin", rodape_style))

    # Gerar PDF
    doc.build(story)

    # Retornar buffer
    buffer.seek(0)
    return buffer.getvalue()

# Configuração da página com melhorias
st.set_page_config(
    page_title='Metodologia FELKLA - Avaliação de Projetos',
    page_icon='🌲',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# CSS customizado com cores da Klabin
st.markdown("""
<style>
    /* Estilo geral da aplicação */
    .main-header {
        background: linear-gradient(90deg, #006837 0%, #228B22 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .main-title {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }

    .main-subtitle {
        color: #e8f5e8;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }

    /* Estilo das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 24px;
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #006837 0%, #228B22 100%);
        color: white !important;
        border-color: #006837;
    }

    /* Estilo das seções */
    .section-header {
        background: linear-gradient(90deg, #f0f8f0 0%, #e8f5e8 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #006837;
        margin-bottom: 1rem;
        font-weight: bold;
        font-size: 1.1rem;
        color: #2d5016;
    }

    /* Melhorias nos selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #006837;
        box-shadow: 0 0 0 2px rgba(0, 104, 55, 0.1);
    }

    /* Estilo dos botões */
    .stButton > button {
        background: linear-gradient(90deg, #006837 0%, #228B22 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #004d28 0%, #1a6b1a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Estilo das métricas */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-top: 3px solid #006837;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #006837;
        font-weight: bold;
    }

    /* Divisores personalizados */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #006837 50%, transparent 100%);
        border: none;
        margin: 2rem 0;
    }

    /* Alertas personalizados */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Cores específicas para alertas */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #006837;
        color: #155724;
    }

    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }

    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }

    /* Estilo para headers das seções */
    .question-section {
        background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #e8f5e8;
        box-shadow: 0 2px 4px rgba(0, 104, 55, 0.05);
    }

    /* Melhorias no layout geral */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal da aplicação
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌲 METODOLOGIA FELKLA</h1>
    <p class="main-subtitle">Sistema de Avaliação e Gestão de Projetos - Klabin</p>
</div>
""", unsafe_allow_html=True)

# NOVO: Seção de identificação do projeto
st.markdown("""
<div style="background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%); 
            padding: 1.5rem; border-radius: 10px; margin: 2rem 0; 
            border-left: 5px solid #006837;">
    <h3 style="color: #006837; margin: 0;">📋 IDENTIFICAÇÃO DO PROJETO</h3>
    <p style="color: #2d5016; margin: 0.5rem 0 0 0;">
        Preencha as informações básicas para identificação da avaliação
    </p>
</div>
""", unsafe_allow_html=True)

# Formulário de identificação
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    nome_projeto = st.text_input(
        "🏗️ **Nome do Projeto**",
        placeholder="Ex: Modernização Linha de Produção 3",
        help="Digite o nome completo do projeto que está sendo avaliado"
    )

    nome_avaliador = st.text_input(
        "�� **Nome do Avaliador**",  # ← CORRIGIDO: emoji funcionando
        placeholder="Ex: João Silva",
        help="Digite seu nome completo"
    )

with col_info2:
    tipo_avaliacao = st.selectbox(
        "📊 **Tipo de Avaliação**",
        ["FELKLA-1", "FELKLA-2", "FELKLA-3"],
        help="Selecione qual fase da metodologia está sendo avaliada"
    )

    data_avaliacao = st.date_input(
        "�� **Data da Avaliação**",
        help="Selecione a data da avaliação"
    )

with col_info3:
    area_responsavel = st.text_input(
        "🏢 **Área Responsável**",
        placeholder="Ex: Engenharia Industrial",
        help="Digite a área ou departamento responsável pelo projeto"
    )

    codigo_projeto = st.text_input(
        "🔢 **Código do Projeto** (opcional)",
        placeholder="Ex: PROJ-2024-001",
        help="Digite o código interno do projeto, se houver"
    )

# Validação dos campos obrigatórios
campos_obrigatorios_preenchidos = bool(nome_projeto and nome_avaliador and tipo_avaliacao and data_avaliacao)

if not campos_obrigatorios_preenchidos:
    st.warning(
        "⚠️ **Atenção:** Preencha pelo menos o nome do projeto, nome do avaliador e tipo de avaliação para continuar.")

st.markdown("---")

# Seção de critérios de avaliação expansível
with st.expander("📋 **CRITÉRIOS DETALHADOS DE AVALIAÇÃO FELKLA**", expanded=False):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: #006837; text-align: center; margin-bottom: 1.5rem;">
            📋 Guia de Pontuação para Avaliações
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                    border-left: 4px solid #28a745; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: #155724; margin-top: 0;">🟢 Pontuação 5 - EXCELENTE</h4>
            <p><strong>Evidências Necessárias:</strong></p>
            <ul style="color: #155724;">
                <li>Documentação completa e aprovada pelos stakeholders</li>
                <li>Análises realizadas com metodologia adequada</li>
                <li>Resultados validados por especialistas</li>
                <li>Aprovação formal da liderança/comitê</li>
                <li>Benchmarks ou melhores práticas considerados</li>
            </ul>
            <div style="background: rgba(21, 87, 36, 0.1); padding: 0.8rem; border-radius: 5px; margin-top: 0.5rem;">
                <strong>Exemplo:</strong> <em>"Estudo de viabilidade econômica concluído com VPL, TIR, payback e cenários de sensibilidade, validado pela área financeira e aprovado pelo comitê."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    border-left: 4px solid #ffc107; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: #856404; margin-top: 0;">🟡 Pontuação 3 - REGULAR</h4>
            <p><strong>Evidências Necessárias:</strong></p>
            <ul style="color: #856404;">
                <li>Trabalho iniciado com progresso significativo (50-79%)</li>
                <li>Estrutura básica estabelecida</li>
                <li>Algumas análises completas, outras em andamento</li>
                <li>Lacunas identificadas com plano para resolução</li>
                <li>Recursos alocados para conclusão</li>
            </ul>
            <div style="background: rgba(133, 100, 4, 0.1); padding: 0.8rem; border-radius: 5px; margin-top: 0.5rem;">
                <strong>Exemplo:</strong> <em>"Mapeamento de riscos identificou principais riscos técnicos e comerciais, mas faltam quantificação de impactos e planos de mitigação detalhados."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                    border-left: 4px solid #dc3545; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: #721c24; margin-top: 0;">🔴 Pontuação 1 - NÃO INICIADO</h4>
            <p><strong>Evidências Necessárias:</strong></p>
            <ul style="color: #721c24;">
                <li>Atividade não foi iniciada (0-19%)</li>
                <li>Apenas intenções ou ideias preliminares</li>
                <li>Falta de recursos ou priorização</li>
                <li>Não aplicável ao tipo específico de projeto</li>
                <li>Dependência de outras atividades não concluídas</li>
            </ul>
            <div style="background: rgba(114, 28, 36, 0.1); padding: 0.8rem; border-radius: 5px; margin-top: 0.5rem;">
                <strong>Exemplo:</strong> <em>"Projeto na fase de ideação, com apenas conceitos preliminares, aguardando aprovação de recursos para iniciar estudos."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #cce5ff 0%, #b3d9ff 100%); 
                    border-left: 4px solid #007bff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: #004085; margin-top: 0;">🔵 Pontuação 4 - BOM</h4>
            <p><strong>Evidências Necessárias:</strong></p>
            <ul style="color: #004085;">
                <li>Trabalho substancialmente completo (80-99%)</li>
                <li>Pequenos ajustes ou complementações pendentes</li>
                <li>Qualidade técnica adequada</li>
                <li>Revisão técnica realizada</li>
                <li>Cronograma para finalização definido</li>
            </ul>
            <div style="background: rgba(0, 64, 133, 0.1); padding: 0.8rem; border-radius: 5px; margin-top: 0.5rem;">
                <strong>Exemplo:</strong> <em>"Análise de alternativas tecnológicas 90% completa, faltando apenas validação final dos custos de uma opção, com conclusão em 1 semana."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffd6cc 0%, #ffb3b3 100%); 
                    border-left: 4px solid #fd7e14; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4 style="color: #8b4513; margin-top: 0;">🟠 Pontuação 2 - INADEQUADO</h4>
            <p><strong>Evidências Necessárias:</strong></p>
            <ul style="color: #8b4513;">
                <li>Trabalho iniciado mas com grandes lacunas (20-49%)</li>
                <li>Informações preliminares disponíveis</li>
                <li>Metodologia definida mas não aplicada completamente</li>
                <li>Necessidade de recursos adicionais significativos</li>
                <li>Cronograma para conclusão indefinido ou muito extenso</li>
            </ul>
            <div style="background: rgba(139, 69, 19, 0.1); padding: 0.8rem; border-radius: 5px; margin-top: 0.5rem;">
                <strong>Exemplo:</strong> <em>"Levantamento de fornecedores iniciado, mas apenas 3 empresas contactadas de um universo de 15 identificadas como relevantes."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Dicas importantes
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #d4f4d4 100%); 
                padding: 1.5rem; border-radius: 8px; margin-top: 1.5rem; 
                border-left: 4px solid #006837;">
        <h4 style="color: #006837; margin-top: 0;">💡 Dicas Importantes para Avaliação:</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <p><strong>🎯 Seja Objetivo:</strong><br>Base sua avaliação em evidências concretas e documentadas</p>
                <p><strong>📝 Documente:</strong><br>Mantenha registros das evidências utilizadas na avaliação</p>
            </div>
            <div>
                <p><strong>🔄 Revise:</strong><br>Reavalie periodicamente conforme o projeto evolui</p>
                <p><strong>⚖️ Consistência:</strong><br>Use os mesmos critérios em todas as avaliações</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Instruções de uso
st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
            padding: 1rem; border-radius: 8px; margin: 1rem 0; 
            border-left: 4px solid #6c757d;">
    <p style="margin: 0; color: #495057;">
        <strong>📖 Instruções:</strong> Responda cada questão selecionando a opção que melhor representa o status atual do seu projeto. 
        Consulte os critérios detalhados acima para uma avaliação precisa e consistente.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Função para calcular pontuação (mantida igual)
def calcular_pontuacao(resposta):
    if resposta == 'Excelente':
        return 5
    elif resposta == 'Bom':
        return 4
    elif resposta == 'Regular':
        return 3
    elif resposta == 'Inadequado':
        return 2
    elif resposta == 'Não iniciado':
        return 1
    else:
        return 0


aba_metodologia, aba1, aba2, aba3 = st.tabs([
    "📚 **METODOLOGIA**",
    "🔍 **FELKLA-1**",
    "⚖️ **FELKLA-2**",
    "✅ **FELKLA-3**"
])

with aba_metodologia:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">📚 METODOLOGIA FELKLA</h2>
        <p style="color: #2d5016; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            <strong>Front-End Loading (FEL)</strong> adaptado para o setor de papel e celulose
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Introdução
    st.markdown("""
    ### 🎯 O que é a Metodologia FELKLA?

    A **Metodologia FELKLA** é uma adaptação da metodologia Front-End Loading (FEL) especificamente desenvolvida para projetos do setor de papel e celulose. 
    Esta abordagem estruturada garante que os projetos sejam adequadamente avaliados, planejados e definidos antes da execução, 
    minimizando riscos e maximizando as chances de sucesso.

    **Benefícios principais:**
    - 🎯 **Redução de riscos** através de planejamento estruturado
    - 💰 **Melhores estimativas** de custo e cronograma  
    - 🔍 **Decisões mais assertivas** baseadas em análises detalhadas
    - 🌱 **Alinhamento** com objetivos de sustentabilidade
    - ⚖️ **Padronização** do processo de avaliação de projetos
    """)

    st.markdown("---")

    # FELKLA-1
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    border: 2px solid #1976d2;">
            <h3 style="color: #1976d2; margin: 0;">🔍 FELKLA-1</h3>
            <p style="color: #1565c0; margin: 0.5rem 0; font-weight: bold;">
                Avaliação de Oportunidades
            </p>
            <p style="color: #1565c0; margin: 0; font-size: 0.9rem;">
                Precisão de Estimativas: ±50%
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        **🎯 Objetivo Principal:**  
        Avaliar a viabilidade técnica e econômica do projeto, definindo se vale a pena prosseguir.

        **📋 Principais Atividades:**
        - Definição do problema/oportunidade de negócio
        - Estudos de mercado e análise de demanda
        - Avaliação de alternativas tecnológicas
        - Estimativas preliminares de CAPEX/OPEX
        - Análise de viabilidade econômica básica
        - Identificação de riscos principais
        - Definição do escopo conceitual

        **📦 Entregáveis:**
        - Documento de definição da oportunidade
        - Estudo de viabilidade preliminar  
        - Estimativa de custos classe 5
        - Cronograma macro
        - Análise de riscos inicial
        """)

    st.markdown("---")

    # FELKLA-2
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    border: 2px solid #f57c00;">
            <h3 style="color: #ef6c00; margin: 0;">⚖️ FELKLA-2</h3>
            <p style="color: #e65100; margin: 0.5rem 0; font-weight: bold;">
                Seleção de Alternativas
            </p>
            <p style="color: #e65100; margin: 0; font-size: 0.9rem;">
                Precisão de Estimativas: ±30%
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        **�� Objetivo Principal:**  
        Selecionar a melhor alternativa técnica e desenvolver o conceito básico do projeto.

        **📋 Principais Atividades:**
        - Desenvolvimento de alternativas técnicas detalhadas
        - Estudos de engenharia básica (fluxogramas, balanços)
        - Seleção de tecnologia e fornecedores principais
        - Definição do layout básico e localização
        - Estimativas de custo mais precisas
        - Análise de riscos detalhada
        - Estudos ambientais e de permissões
        - Estratégia de execução preliminar

        **📦 Entregáveis:**
        - Documento de seleção de alternativa
        - Fluxogramas de processo (PFDs)
        - Layout preliminar do projeto
        - Estimativa de custos classe 4
        - Cronograma detalhado
        - Plano de gerenciamento de riscos
        - Estudos de impacto ambiental
        """)

    st.markdown("---")

    # FELKLA-3
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    border: 2px solid #388e3c;">
            <h3 style="color: #2e7d32; margin: 0;">✅ FELKLA-3</h3>
            <p style="color: #1b5e20; margin: 0.5rem 0; font-weight: bold;">
                Definição do Projeto
            </p>
            <p style="color: #1b5e20; margin: 0; font-size: 0.9rem;">
                Precisão de Estimativas: ±15%
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        **🎯 Objetivo Principal:**  
        Definir completamente o projeto antes da execução, minimizando mudanças durante a construção.

        **📋 Principais Atividades:**
        - Engenharia de detalhe avançada (P&IDs, especificações)
        - Definição completa do escopo de trabalho
        - Cotações firmes de equipamentos principais
        - Plano de execução detalhado
        - Estimativas de custo de alta precisão
        - Cronograma executivo detalhado
        - Planos de qualidade, segurança e meio ambiente
        - Estratégia de contratação e aquisições
        - Obtenção de licenças e permissões

        **📦 Entregáveis:**
        - Pacote completo de engenharia básica
        - P&IDs (Piping & Instrumentation Diagrams)
        - Especificações técnicas detalhadas
        - Estimativa de custos classe 3
        - Cronograma executivo
        - Plano de execução do projeto
        - Contratos principais negociados
        - Todas as licenças aprovadas
        """)

    st.markdown("---")

    # Fluxo da metodologia
    st.markdown("### 🔄 Fluxo da Metodologia FELKLA")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 2rem; border-radius: 10px; margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="text-align: center; margin: 0.5rem;">
                <div style="background: #1976d2; color: white; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem;">
                    <strong>F1</strong>
                </div>
                <p style="margin: 0; font-weight: bold;">Oportunidade</p>
            </div>
            <div style="font-size: 2rem; color: #006837;">→</div>
            <div style="text-align: center; margin: 0.5rem;">
                <div style="background: #f57c00; color: white; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem;">
                    <strong>F2</strong>
                </div>
                <p style="margin: 0; font-weight: bold;">Seleção</p>
            </div>
            <div style="font-size: 2rem; color: #006837;">→</div>
            <div style="text-align: center; margin: 0.5rem;">
                <div style="background: #388e3c; color: white; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem;">
                    <strong>F3</strong>
                </div>
                <p style="margin: 0; font-weight: bold;">Definição</p>
            </div>
            <div style="font-size: 2rem; color: #006837;">→</div>
            <div style="text-align: center; margin: 0.5rem;">
                <div style="background: #006837; color: white; padding: 1rem; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem;">
                    <strong>🚀</strong>
                </div>
                <p style="margin: 0; font-weight: bold;">Execução</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Critérios de aprovação
    st.markdown("### ✅ Critérios de Aprovação por Fase")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🔍 FELKLA-1**
        - Score ≥ 80%: Aprovado para F2
        - Score 60-79%: Melhorias necessárias
        - Score < 60%: Não recomendado
        """)

    with col2:
        st.markdown("""
        **⚖️ FELKLA-2**
        - Score ≥ 80%: Aprovado para F3
        - Score 60-79%: Ajustes necessários
        - Score < 60%: Retornar ao F1
        """)

    with col3:
        st.markdown("""
        **✅ FELKLA-3**
        - Score ≥ 80%: Pronto para execução
        - Score 60-79%: Finalizar pendências
        - Score < 60%: Revisar projeto
        """)

    # Nota importante
    st.info("""
    💡 **Nota Importante:** Esta metodologia foi especificamente adaptada para o setor de papel e celulose, 
    considerando as particularidades técnicas, ambientais e regulatórias desta indústria.
    """)

with aba1:
    # Header da aba com informações
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">🔍 QUESTIONÁRIO FELKLA-1</h2>
        <p style="color: #2d5016; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            <strong>Objetivo:</strong> Avaliar a viabilidade inicial e oportunidades do projeto
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Indicador de progresso
    st.markdown("### 📊 Progresso do Questionário")
    progress_placeholder = st.empty()

    # Função para contar respostas preenchidas
    def contar_respostas_aba1():
        respostas = [q11, q12, q13, q14, q15, q21, q22, q23, q24, q25,
                    q31, q32, q33, q34, q35, q41, q42, q43, q44, q45,
                    q51, q52, q53, q54, q55]
        preenchidas = len([r for r in respostas if r is not None])
        return preenchidas, len(respostas)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🎯 DEFINIÇÃO DA OPORTUNIDADE
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 20%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q11 = st.selectbox(
            '**1.1** O problema/oportunidade de negócio está claramente definido e documentado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se o problema ou oportunidade está bem documentado e compreendido"
        )

        q12 = st.selectbox(
            '**1.2** Os objetivos do projeto estão alinhados com a estratégia corporativa e metas de sustentabilidade?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique o alinhamento estratégico e sustentável do projeto"
        )

        q13 = st.selectbox(
            '**1.3** O escopo preliminar do projeto foi estabelecido (o que está incluído/excluído)?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se o escopo está bem definido com inclusões e exclusões claras"
        )

        q14 = st.selectbox(
            '**1.4** Os stakeholders principais foram identificados e suas necessidades mapeadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se todos os stakeholders relevantes foram identificados"
        )

        q15 = st.selectbox(
            '**1.5** Os drivers de negócio (regulatório, competitivo, operacional) foram caracterizados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se os motivadores do projeto estão bem caracterizados"
        )

    with col2:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🔧 VIABILIDADE TÉCNICA
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 20%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q21 = st.selectbox(
            '**2.1** As alternativas tecnológicas disponíveis foram identificadas e avaliadas preliminarmente?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se diferentes opções tecnológicas foram consideradas"
        )

        q22 = st.selectbox(
            '**2.2** A compatibilidade com sistemas/processos existentes foi analisada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie a integração com a infraestrutura atual"
        )

        q23 = st.selectbox(
            '**2.3** Os recursos técnicos necessários (expertise, infraestrutura) foram avaliados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se os recursos técnicos necessários foram mapeados"
        )

        q24 = st.selectbox(
            '**2.4** Restrições técnicas e limitações foram identificadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se as limitações técnicas estão mapeadas"
        )

        q25 = st.selectbox(
            '**2.5** A maturidade tecnológica das soluções propostas foi verificada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique o nível de maturidade das tecnologias propostas"
        )

    # Divisor visual personalizado
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                💰 VIABILIDADE ECONÔMICA
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 25%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q31 = st.selectbox(
            '**3.1** Estimativa preliminar de investimento (CAPEX) foi elaborada com metodologia adequada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie a qualidade das estimativas de investimento inicial"
        )

        q32 = st.selectbox(
            '**3.2** Impactos operacionais (OPEX) foram estimados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se os custos operacionais foram considerados"
        )

        q33 = st.selectbox(
            '**3.3** Benefícios esperados foram quantificados (receitas, economias, evitação de custos)?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se os benefícios financeiros estão quantificados"
        )

        q34 = st.selectbox(
            '**3.4** Análise econômica básica (VPL, TIR, payback) foi realizada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se indicadores econômicos foram calculados"
        )

        q35 = st.selectbox(
            '**3.5** Sensibilidades e cenários econômicos foram considerados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se diferentes cenários econômicos foram analisados"
        )

    with col4:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🌱 ASPECTOS AMBIENTAIS E REGULATÓRIOS
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 20%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q41 = st.selectbox(
            '**4.1** Requisitos regulatórios e de licenciamento foram identificados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se todos os requisitos legais foram mapeados"
        )

        q42 = st.selectbox(
            '**4.2** Impactos ambientais potenciais foram mapeados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se os impactos ambientais foram identificados"
        )

        q43 = st.selectbox(
            '**4.3** Necessidades de certificações/autorizações foram levantadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se certificações necessárias foram identificadas"
        )

        q44 = st.selectbox(
            '**4.4** Conformidade com políticas internas de sustentabilidade foi verificada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie o alinhamento com políticas de sustentabilidade"
        )

        q45 = st.selectbox(
            '**4.5** Stakeholders externos relevantes foram identificados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se stakeholders externos foram mapeados"
        )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="question-section">
        <h3 style="color: #006837; margin-bottom: 1rem;">
            ⚠️ RISCOS E CRONOGRAMA
            <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                  border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 15%</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col5, col6, col7 = st.columns([1, 1, 1])

    with col5:
        q51 = st.selectbox(
            '**5.1** Principais riscos do projeto foram identificados e categorizados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se os riscos principais foram mapeados"
        )

        q52 = st.selectbox(
            '**5.2** Cronograma macro foi estabelecido com marcos principais?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se existe um cronograma preliminar"
        )

    with col6:
        q53 = st.selectbox(
            '**5.3** Dependências críticas foram mapeadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se dependências críticas foram identificadas"
        )

        q54 = st.selectbox(
            '**5.4** Recursos necessários (humanos, financeiros) foram estimados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Verifique se recursos necessários foram estimados"
        )

    with col7:
        q55 = st.selectbox(
            '**5.5** Critérios de sucesso foram definidos?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            help="Avalie se critérios de sucesso estão definidos"
        )

    # Atualizar progresso
    preenchidas, total = contar_respostas_aba1()
    progress_percentage = preenchidas / total

    with progress_placeholder:
        st.progress(progress_percentage, text=f"Progresso: {preenchidas}/{total} questões respondidas ({progress_percentage:.1%})")

        if preenchidas < total:
            st.info(f"💡 **Dica:** Responda todas as {total} questões para obter uma avaliação completa!")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    # Seção de resultados melhorada
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin: 2rem 0; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">📊 RELATÓRIO FELKLA-1</h2>
        <p style="color: #2d5016; margin: 0.5rem 0; font-size: 1.1rem;">
            Análise detalhada da viabilidade e oportunidades do projeto
        </p>
        <div style="margin-top: 1rem; color: #2d5016;">
            <p style="margin: 0.3rem 0;"><strong>Projeto:</strong> {nome_projeto or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Avaliador:</strong> {nome_avaliador or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Data:</strong> {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}</p>
            <p style="margin: 0.3rem 0;"><strong>Área:</strong> {area_responsavel or 'Não informada'}</p>
            {f'<p style="margin: 0.3rem 0;"><strong>Código:</strong> {codigo_projeto}</p>' if codigo_projeto else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Verificar se todas as questões foram respondidas
    todas_respostas = [q11, q12, q13, q14, q15, q21, q22, q23, q24, q25,
                       q31, q32, q33, q34, q35, q41, q42, q43, q44, q45,
                       q51, q52, q53, q54, q55]

    respostas_preenchidas = [r for r in todas_respostas if r is not None]

    # Inicializar variáveis
    calcular_resultado = False

    if len(respostas_preenchidas) == 0:
        st.info("🔍 **Responda as questões acima para gerar o resultado da avaliação FELKLA-1**")

    elif len(respostas_preenchidas) < len(todas_respostas):
        col_aviso1, col_aviso2 = st.columns([2, 1])
        with col_aviso1:
            st.warning(
                f"⚠️ **Atenção:** {len(todas_respostas) - len(respostas_preenchidas)} questões ainda não foram respondidas. Para uma avaliação completa, responda todas as questões.")
        with col_aviso2:
            calcular_resultado = st.button("📊 Calcular Resultado Parcial", type="secondary")

    else:
        # Todas as questões respondidas
        calcular_resultado = st.button("🚀 Calcular Resultado Completo FELKLA-1", type="primary")

    if calcular_resultado:
        # Cálculos dos scores
        # Definição da Oportunidade (20%)
        def_oport = [q11, q12, q13, q14, q15]
        pontos_def = sum([calcular_pontuacao(resp) for resp in def_oport if resp is not None])
        max_pontos_def = len([resp for resp in def_oport if resp is not None]) * 5
        score_def = (pontos_def / max_pontos_def * 100) if max_pontos_def > 0 else 0

        # Viabilidade Técnica (20%)
        viab_tec = [q21, q22, q23, q24, q25]
        pontos_tec = sum([calcular_pontuacao(resp) for resp in viab_tec if resp is not None])
        max_pontos_tec = len([resp for resp in viab_tec if resp is not None]) * 5
        score_tec = (pontos_tec / max_pontos_tec * 100) if max_pontos_tec > 0 else 0

        # Viabilidade Econômica (25%)
        viab_eco = [q31, q32, q33, q34, q35]
        pontos_eco = sum([calcular_pontuacao(resp) for resp in viab_eco if resp is not None])
        max_pontos_eco = len([resp for resp in viab_eco if resp is not None]) * 5
        score_eco = (pontos_eco / max_pontos_eco * 100) if max_pontos_eco > 0 else 0

        # Aspectos Ambientais (20%)
        asp_amb = [q41, q42, q43, q44, q45]
        pontos_amb = sum([calcular_pontuacao(resp) for resp in asp_amb if resp is not None])
        max_pontos_amb = len([resp for resp in asp_amb if resp is not None]) * 5
        score_amb = (pontos_amb / max_pontos_amb * 100) if max_pontos_amb > 0 else 0

        # Riscos e Cronograma (15%)
        risco_cron = [q51, q52, q53, q54, q55]
        pontos_risco = sum([calcular_pontuacao(resp) for resp in risco_cron if resp is not None])
        max_pontos_risco = len([resp for resp in risco_cron if resp is not None]) * 5
        score_risco = (pontos_risco / max_pontos_risco * 100) if max_pontos_risco > 0 else 0

        # Score Final Ponderado
        score_final = (score_def * 0.20 + score_tec * 0.20 + score_eco * 0.25 +
                       score_amb * 0.20 + score_risco * 0.15)

        # Dashboard de resultados
        st.markdown("### 📈 Dashboard de Resultados")

        # Métricas principais em cards
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

        with col_m1:
            delta_def = "🎯" if score_def >= 80 else "⚠️" if score_def >= 60 else "❌"
            st.metric(
                "Definição da Oportunidade",
                f"{score_def:.1f}%",
                delta=f"Peso: 20% {delta_def}"
            )

        with col_m2:
            delta_tec = "🎯" if score_tec >= 80 else "⚠️" if score_tec >= 60 else "❌"
            st.metric(
                "Viabilidade Técnica",
                f"{score_tec:.1f}%",
                delta=f"Peso: 20% {delta_tec}"
            )

        with col_m3:
            delta_eco = "🎯" if score_eco >= 80 else "⚠️" if score_eco >= 60 else "❌"
            st.metric(
                "Viabilidade Econômica",
                f"{score_eco:.1f}%",
                delta=f"Peso: 25% {delta_eco}"
            )

        with col_m4:
            delta_amb = "🎯" if score_amb >= 80 else "⚠️" if score_amb >= 60 else "❌"
            st.metric(
                "Aspectos Ambientais",
                f"{score_amb:.1f}%",
                delta=f"Peso: 20% {delta_amb}"
            )

        with col_m5:
            delta_risco = "🎯" if score_risco >= 80 else "⚠️" if score_risco >= 60 else "❌"
            st.metric(
                "Riscos e Cronograma",
                f"{score_risco:.1f}%",
                delta=f"Peso: 15% {delta_risco}"
            )

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        # Score final destacado
        col_score, col_interpretation = st.columns([1, 2])

        with col_score:
            if score_final >= 80:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #006837; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #006837; margin: 0; font-size: 3rem;">{score_final:.1f}%</h1>
                        <h3 style="color: #155724; margin: 0.5rem 0;">✅ APROVADO</h3>
                        <p style="color: #155724; margin: 0;">Projeto pronto para FELKLA-2</p>
                    </div>
                    """, unsafe_allow_html=True)
            elif score_final >= 60:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #ffc107; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #856404; margin: 0; font-size: 3rem;">{score_final:.1f}%</h1>
                        <h3 style="color: #856404; margin: 0.5rem 0;">⚠️ ATENÇÃO</h3>
                        <p style="color: #856404; margin: 0;">Projeto necessita melhorias</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #dc3545; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #721c24; margin: 0; font-size: 3rem;">{score_final:.1f}%</h1>
                        <h3 style="color: #721c24; margin: 0.5rem 0;">❌ NÃO APROVADO</h3>
                        <p style="color: #721c24; margin: 0;">Projeto não recomendado</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_interpretation:
            st.markdown("#### �� Interpretação dos Resultados")

            if score_final >= 80:
                st.success("""
                    **Excelente! Projeto aprovado para próxima fase**

                    ✅ **Recomendações:**
                    - Prosseguir para FELKLA-2
                    - Manter qualidade dos estudos
                    - Documentar lições aprendidas
                    """)
            elif score_final >= 60:
                st.warning("""
                    **Projeto viável com melhorias necessárias**

                    ⚠️ **Ações recomendadas:**
                    - Revisar áreas com pontuação baixa
                    - Aprofundar estudos deficientes
                    - Buscar suporte técnico especializado
                    """)
            else:
                st.error("""
                    **Projeto não recomendado no momento**

                    ❌ **Ações necessárias:**
                    - Revisão completa do escopo
                    - Reavaliação da viabilidade
                    - Considerar alternativas ou cancelamento
                    """)

        # Análise detalhada por dimensão
        st.markdown("#### 📊 Análise Detalhada por Dimensão")

        # Identificar pontos fortes e fracos
        scores = {
            "Definição da Oportunidade": score_def,
            "Viabilidade Técnica": score_tec,
            "Viabilidade Econômica": score_eco,
            "Aspectos Ambientais": score_amb,
            "Riscos e Cronograma": score_risco
        }

        pontos_fortes = [k for k, v in scores.items() if v >= 80]
        pontos_atenção = [k for k, v in scores.items() if 60 <= v < 80]
        pontos_críticos = [k for k, v in scores.items() if v < 60]

        col_analise1, col_analise2, col_analise3 = st.columns(3)

        with col_analise1:
            if pontos_fortes:
                st.markdown("**🟢 Pontos Fortes**")
                for ponto in pontos_fortes:
                    st.markdown(f"✅ {ponto}")
            else:
                st.markdown("**🟢 Pontos Fortes**")
                st.markdown("_Nenhum identificado_")

        with col_analise2:
            if pontos_atenção:
                st.markdown("**🟡 Necessita Atenção**")
                for ponto in pontos_atenção:
                    st.markdown(f"⚠️ {ponto}")
            else:
                st.markdown("**🟡 Necessita Atenção**")
                st.markdown("_Nenhum identificado_")

        with col_analise3:
            if pontos_críticos:
                st.markdown("**🔴 Pontos Críticos**")
                for ponto in pontos_críticos:
                    st.markdown(f"❌ {ponto}")
            else:
                st.markdown("**🔴 Pontos Críticos**")
                st.markdown("_Nenhum identificado_")

        # Próximos passos (FORA de todas as colunas)
        st.markdown("#### 🚀 Próximos Passos Recomendados")

        if score_final >= 80:
            st.info("""
                1. **Documentar resultados** da avaliação FELKLA-1
                2. **Preparar documentação** para FELKLA-2
                3. **Alocar recursos** para próxima fase
                4. **Agendar reunião** de aprovação para FELKLA-2
                """)
        elif score_final >= 60:
            st.warning("""
                1. **Priorizar melhorias** nas áreas críticas identificadas
                2. **Buscar suporte técnico** especializado
                3. **Revisar cronograma** considerando melhorias
                4. **Reavaliar** após implementação das melhorias
                """)
        else:
            st.error("""
                1. **Revisar fundamentação** do projeto
                2. **Considerar alternativas** de escopo ou abordagem
                3. **Avaliar viabilidade** de continuidade
                4. **Documentar lições aprendidas** para projetos futuros
                """)

        # Download do Relatório FELKLA-1
        st.markdown("---")

        # Verificar se campos obrigatórios estão preenchidos
        campos_obrigatorios_preenchidos = bool(nome_projeto and nome_avaliador and data_avaliacao and area_responsavel)

        if campos_obrigatorios_preenchidos:
            # Gerar relatório em texto
            relatorio_texto = f"""
RELATÓRIO DE AVALIAÇÃO FELKLA-1
=====================================

IDENTIFICAÇÃO DO PROJETO:
- Nome do Projeto: {nome_projeto}
- Avaliador: {nome_avaliador}
- Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}
- Área Responsável: {area_responsavel}
{f'- Código do Projeto: {codigo_projeto}' if codigo_projeto else ''}

RESULTADO DA AVALIAÇÃO:
- Score Final: {score_final:.1f}%
- Status: {'APROVADO' if score_final >= 80 else 'ATENÇÃO' if score_final >= 60 else 'NÃO APROVADO'}
- Questões Respondidas: {len(respostas_preenchidas)}/{len(todas_respostas)}

DETALHAMENTO POR DIMENSÃO:
- Definição da Oportunidade: {score_def:.1f}%
- Viabilidade Técnica: {score_tec:.1f}%
- Viabilidade Econômica: {score_eco:.1f}%
- Aspectos Ambientais: {score_amb:.1f}%
- Riscos e Cronograma: {score_risco:.1f}%

ANÁLISE:
- Pontos Fortes: {', '.join(pontos_fortes) if pontos_fortes else 'Nenhum identificado'}
- Pontos de Atenção: {', '.join(pontos_atenção) if pontos_atenção else 'Nenhum identificado'}
- Pontos Críticos: {', '.join(pontos_críticos) if pontos_críticos else 'Nenhum identificado'}

PRÓXIMOS PASSOS:
{'- Prosseguir para FELKLA-2' if score_final >= 80 else '- Melhorar áreas críticas identificadas' if score_final >= 60 else '- Revisar fundamentação do projeto'}

Relatório gerado automaticamente pela Metodologia FELKLA - Klabin
Data de geração: {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}
            """

            try:
                # Gerar PDF
                nome_arquivo = f"Relatorio_FELKLA-1_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.pdf"
                pdf_bytes = gerar_pdf_relatorio(relatorio_texto, nome_arquivo)

                st.markdown("#### 📥 Download do Relatório")
                col_download1, col_download2 = st.columns(2)

                with col_download1:
                    st.download_button(
                        label="📄 Download Relatório FELKLA-1 (.pdf)",
                        data=pdf_bytes,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )

                with col_download2:
                    st.button("�� Enviar por Email", help="Funcionalidade em desenvolvimento")

            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
                # Fallback para TXT
                st.download_button(
                    label="📄 Download Relatório FELKLA-1 (.txt)",
                    data=relatorio_texto,
                    file_name=f"Relatorio_FELKLA-1_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.txt",
                    mime="text/plain"
                )
        else:
            st.info("💡 **Dica:** Preencha as informações do projeto no topo da página para habilitar o download do relatório.")




with aba2:
    # Header da aba com informações
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">⚖️ QUESTIONÁRIO FELKLA-2</h2>
        <p style="color: #2d5016; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            <strong>Objetivo:</strong> Seleção e desenvolvimento de alternativas técnicas
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Indicador de progresso
    st.markdown("### 📊 Progresso do Questionário")
    progress_placeholder_2 = st.empty()


    # Função para contar respostas preenchidas FELKLA-2
    def contar_respostas_aba2():
        respostas = [q11_f2, q12_f2, q13_f2, q14_f2, q15_f2, q21_f2, q22_f2, q23_f2, q24_f2, q25_f2,
                     q31_f2, q32_f2, q33_f2, q34_f2, q35_f2, q41_f2, q42_f2, q43_f2, q44_f2, q45_f2,
                     q51_f2, q52_f2, q53_f2, q54_f2, q55_f2]
        preenchidas = len([r for r in respostas if r is not None])
        return preenchidas, len(respostas)


    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🔧 DESENVOLVIMENTO TÉCNICO
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 30%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q11_f2 = st.selectbox(
            '**1.1** Alternativas técnicas foram desenvolvidas em nível adequado de detalhe?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q11',
            help="Avalie o nível de detalhamento das alternativas técnicas"
        )

        q12_f2 = st.selectbox(
            '**1.2** Estudos de engenharia básica foram realizados conforme necessário?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q12',
            help="Verifique a qualidade dos estudos de engenharia básica"
        )

        q13_f2 = st.selectbox(
            '**1.3** Interfaces com sistemas existentes foram definidas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q13',
            help="Avalie se as interfaces estão bem definidas"
        )

        q14_f2 = st.selectbox(
            '**1.4** Especificações técnicas preliminares foram elaboradas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q14',
            help="Verifique a qualidade das especificações técnicas"
        )

        q15_f2 = st.selectbox(
            '**1.5** Análise de capacidade e performance foi realizada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q15',
            help="Avalie se a capacidade e performance foram analisadas"
        )

    with col2:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                ⚖️ SELEÇÃO DE SOLUÇÕES
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 25%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q21_f2 = st.selectbox(
            '**2.1** Critérios de seleção foram estabelecidos e aplicados consistentemente?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q21',
            help="Verifique se critérios claros foram estabelecidos"
        )

        q22_f2 = st.selectbox(
            '**2.2** Fornecedores/tecnologias foram pré-qualificados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q22',
            help="Avalie o processo de pré-qualificação"
        )

        q23_f2 = st.selectbox(
            '**2.3** Análise comparativa das alternativas foi documentada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q23',
            help="Verifique se existe documentação da análise comparativa"
        )

        q24_f2 = st.selectbox(
            '**2.4** Solução preferencial foi selecionada com justificativa técnico-econômica?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q24',
            help="Avalie se a seleção tem justificativa adequada"
        )

        q25_f2 = st.selectbox(
            '**2.5** Estratégia de implementação foi definida?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q25',
            help="Verifique se a estratégia de implementação está clara"
        )

    # Divisor visual personalizado
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🏗️ PLANEJAMENTO E LAYOUT
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 20%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q31_f2 = st.selectbox(
            '**3.1** Layout/arranjo físico foi desenvolvido adequadamente?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q31',
            help="Avalie a qualidade do layout desenvolvido"
        )

        q32_f2 = st.selectbox(
            '**3.2** Necessidades de infraestrutura foram identificadas e dimensionadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q32',
            help="Verifique se a infraestrutura foi adequadamente dimensionada"
        )

        q33_f2 = st.selectbox(
            '**3.3** Integração com operações existentes foi planejada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q33',
            help="Avalie o planejamento da integração operacional"
        )

        q34_f2 = st.selectbox(
            '**3.4** Logística de materiais e produtos foi considerada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q34',
            help="Verifique se aspectos logísticos foram considerados"
        )

        q35_f2 = st.selectbox(
            '**3.5** Facilidades de apoio foram dimensionadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q35',
            help="Avalie o dimensionamento das facilidades de apoio"
        )

    with col4:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🌱 ASPECTOS AMBIENTAIS E SOCIAIS
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 15%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q41_f2 = st.selectbox(
            '**4.1** Estudos ambientais necessários foram iniciados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q41',
            help="Verifique o status dos estudos ambientais"
        )

        q42_f2 = st.selectbox(
            '**4.2** Estratégia de licenciamento foi definida?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q42',
            help="Avalie se a estratégia de licenciamento está clara"
        )

        q43_f2 = st.selectbox(
            '**4.3** Impactos sociais foram avaliados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q43',
            help="Verifique se impactos sociais foram considerados"
        )

        q44_f2 = st.selectbox(
            '**4.4** Plano de engajamento de stakeholders foi elaborado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q44',
            help="Avalie o plano de engajamento dos stakeholders"
        )

        q45_f2 = st.selectbox(
            '**4.5** Medidas mitigadoras foram identificadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q45',
            help="Verifique se medidas mitigadoras estão definidas"
        )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="question-section">
        <h3 style="color: #006837; margin-bottom: 1rem;">
            📊 ESTIMATIVAS E GESTÃO DE RISCOS
            <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                  border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 10%</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col5, col6, col7 = st.columns([1, 1, 1])

    with col5:
        q51_f2 = st.selectbox(
            '**5.1** Estimativas de custo foram refinadas com melhor precisão?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q51',
            help="Avalie a precisão das estimativas refinadas"
        )

        q52_f2 = st.selectbox(
            '**5.2** Cronograma detalhado foi desenvolvido?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q52',
            help="Verifique se o cronograma está detalhado"
        )

    with col6:
        q53_f2 = st.selectbox(
            '**5.3** Análise de riscos foi aprofundada com planos de mitigação?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q53',
            help="Avalie a profundidade da análise de riscos"
        )

        q54_f2 = st.selectbox(
            '**5.4** Análise de sensibilidade econômica foi atualizada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q54',
            help="Verifique se a análise de sensibilidade foi atualizada"
        )

    with col7:
        q55_f2 = st.selectbox(
            '**5.5** Métricas de controle do projeto foram definidas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla2_q55',
            help="Avalie se métricas de controle estão definidas"
        )

    # Atualizar progresso
    preenchidas_2, total_2 = contar_respostas_aba2()
    progress_percentage_2 = preenchidas_2 / total_2

    with progress_placeholder_2:
        st.progress(progress_percentage_2,
                    text=f"Progresso: {preenchidas_2}/{total_2} questões respondidas ({progress_percentage_2:.1%})")

        if preenchidas_2 < total_2:
            st.info(f"💡 **Dica:** Responda todas as {total_2} questões para obter uma avaliação completa!")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    # Seção de resultados melhorada FELKLA-2
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin: 2rem 0; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">📊 RELATÓRIO FELKLA-2</h2>
        <p style="color: #2d5016; margin: 0.5rem 0; font-size: 1.1rem;">
            Análise da seleção e desenvolvimento de alternativas técnicas
        </p>
        <div style="margin-top: 1rem; color: #2d5016;">
            <p style="margin: 0.3rem 0;"><strong>Projeto:</strong> {nome_projeto or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Avaliador:</strong> {nome_avaliador or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Data:</strong> {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}</p>
            <p style="margin: 0.3rem 0;"><strong>Área:</strong> {area_responsavel or 'Não informada'}</p>
            {f'<p style="margin: 0.3rem 0;"><strong>Código:</strong> {codigo_projeto}</p>' if codigo_projeto else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Verificar se todas as questões foram respondidas
    todas_respostas_f2 = [q11_f2, q12_f2, q13_f2, q14_f2, q15_f2, q21_f2, q22_f2, q23_f2, q24_f2, q25_f2,
                          q31_f2, q32_f2, q33_f2, q34_f2, q35_f2, q41_f2, q42_f2, q43_f2, q44_f2, q45_f2,
                          q51_f2, q52_f2, q53_f2, q54_f2, q55_f2]

    respostas_preenchidas_f2 = [r for r in todas_respostas_f2 if r is not None]

    # Inicializar variáveis
    calcular_resultado_f2 = False

    if len(respostas_preenchidas_f2) == 0:
        st.info("🔍 **Responda as questões acima para gerar o resultado da avaliação FELKLA-2**")

    elif len(respostas_preenchidas_f2) < len(todas_respostas_f2):
        col_aviso1, col_aviso2 = st.columns([2, 1])
        with col_aviso1:
            st.warning(
                f"⚠️ **Atenção:** {len(todas_respostas_f2) - len(respostas_preenchidas_f2)} questões ainda não foram respondidas. Para uma avaliação completa, responda todas as questões.")
        with col_aviso2:
            calcular_resultado_f2 = st.button("📊 Calcular Resultado Parcial FELKLA-2", type="secondary")

    else:
        # Todas as questões respondidas
        calcular_resultado_f2 = st.button("🚀 Calcular Resultado Completo FELKLA-2", type="primary")

    if calcular_resultado_f2:
        # Cálculos dos scores FELKLA-2
        # Desenvolvimento Técnico (30%)
        dev_tec = [q11_f2, q12_f2, q13_f2, q14_f2, q15_f2]
        pontos_dev = sum([calcular_pontuacao(resp) for resp in dev_tec if resp is not None])
        max_pontos_dev = len([resp for resp in dev_tec if resp is not None]) * 5
        score_dev = (pontos_dev / max_pontos_dev * 100) if max_pontos_dev > 0 else 0

        # Seleção de Soluções (25%)
        sel_sol = [q21_f2, q22_f2, q23_f2, q24_f2, q25_f2]
        pontos_sel = sum([calcular_pontuacao(resp) for resp in sel_sol if resp is not None])
        max_pontos_sel = len([resp for resp in sel_sol if resp is not None]) * 5
        score_sel = (pontos_sel / max_pontos_sel * 100) if max_pontos_sel > 0 else 0

        # Planejamento e Layout (20%)
        plan_lay = [q31_f2, q32_f2, q33_f2, q34_f2, q35_f2]
        pontos_plan = sum([calcular_pontuacao(resp) for resp in plan_lay if resp is not None])
        max_pontos_plan = len([resp for resp in plan_lay if resp is not None]) * 5
        score_plan = (pontos_plan / max_pontos_plan * 100) if max_pontos_plan > 0 else 0

        # Aspectos Ambientais e Sociais (15%)
        asp_amb_soc = [q41_f2, q42_f2, q43_f2, q44_f2, q45_f2]
        pontos_amb_soc = sum([calcular_pontuacao(resp) for resp in asp_amb_soc if resp is not None])
        max_pontos_amb_soc = len([resp for resp in asp_amb_soc if resp is not None]) * 5
        score_amb_soc = (pontos_amb_soc / max_pontos_amb_soc * 100) if max_pontos_amb_soc > 0 else 0

        # Estimativas e Gestão de Riscos (10%)
        est_risco = [q51_f2, q52_f2, q53_f2, q54_f2, q55_f2]
        pontos_est = sum([calcular_pontuacao(resp) for resp in est_risco if resp is not None])
        max_pontos_est = len([resp for resp in est_risco if resp is not None]) * 5
        score_est = (pontos_est / max_pontos_est * 100) if max_pontos_est > 0 else 0

        # Score Final Ponderado
        score_final_f2 = (score_dev * 0.30 + score_sel * 0.25 + score_plan * 0.20 +
                          score_amb_soc * 0.15 + score_est * 0.10)

        # Dashboard de resultados
        st.markdown("### 📈 Dashboard de Resultados FELKLA-2")

        # Métricas principais em cards
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

        with col_m1:
            delta_dev = "🎯" if score_dev >= 80 else "⚠️" if score_dev >= 60 else "❌"
            st.metric(
                "Desenvolvimento Técnico",
                f"{score_dev:.1f}%",
                delta=f"Peso: 30% {delta_dev}"
            )

        with col_m2:
            delta_sel = "🎯" if score_sel >= 80 else "⚠️" if score_sel >= 60 else "❌"
            st.metric(
                "Seleção de Soluções",
                f"{score_sel:.1f}%",
                delta=f"Peso: 25% {delta_sel}"
            )

        with col_m3:
            delta_plan = "🎯" if score_plan >= 80 else "⚠️" if score_plan >= 60 else "❌"
            st.metric(
                "Planejamento e Layout",
                f"{score_plan:.1f}%",
                delta=f"Peso: 20% {delta_plan}"
            )

        with col_m4:
            delta_amb_soc = "🎯" if score_amb_soc >= 80 else "⚠️" if score_amb_soc >= 60 else "❌"
            st.metric(
                "Aspectos Ambientais/Sociais",
                f"{score_amb_soc:.1f}%",
                delta=f"Peso: 15% {delta_amb_soc}"
            )

        with col_m5:
            delta_est = "🎯" if score_est >= 80 else "⚠️" if score_est >= 60 else "❌"
            st.metric(
                "Estimativas e Riscos",
                f"{score_est:.1f}%",
                delta=f"Peso: 10% {delta_est}"
            )

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        # Score final destacado
        col_score, col_interpretation = st.columns([1, 2])

        with col_score:
            if score_final_f2 >= 80:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #006837; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #006837; margin: 0; font-size: 3rem;">{score_final_f2:.1f}%</h1>
                        <h3 style="color: #155724; margin: 0.5rem 0;">✅ APROVADO</h3>
                        <p style="color: #155724; margin: 0;">Projeto pronto para FELKLA-3</p>
                    </div>
                    """, unsafe_allow_html=True)
            elif score_final_f2 >= 60:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #ffc107; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #856404; margin: 0; font-size: 3rem;">{score_final_f2:.1f}%</h1>
                        <h3 style="color: #856404; margin: 0.5rem 0;">⚠️ ATENÇÃO</h3>
                        <p style="color: #856404; margin: 0;">Projeto necessita melhorias</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #dc3545; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #721c24; margin: 0; font-size: 3rem;">{score_final_f2:.1f}%</h1>
                        <h3 style="color: #721c24; margin: 0.5rem 0;">❌ NÃO APROVADO</h3>
                        <p style="color: #721c24; margin: 0;">Projeto não recomendado</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_interpretation:
            st.markdown("#### 🎯 Interpretação dos Resultados")

            if score_final_f2 >= 80:
                st.success("""
                    **Excelente! Projeto aprovado para FELKLA-3**

                    ✅ **Recomendações:**
                    - Prosseguir para fase de definição do projeto
                    - Manter qualidade dos estudos técnicos
                    - Finalizar seleção de fornecedores
                    """)
            elif score_final_f2 >= 60:
                st.warning("""
                    **Projeto viável com melhorias necessárias**

                    ⚠️ **Ações recomendadas:**
                    - Aprofundar desenvolvimento técnico
                    - Revisar critérios de seleção
                    - Melhorar planejamento de layout
                    """)
            else:
                st.error("""
                    **Projeto não recomendado para próxima fase**

                    ❌ **Ações necessárias:**
                    - Revisar alternativas técnicas
                    - Reavaliar viabilidade das soluções
                    - Considerar retorno ao FELKLA-1
                    """)

        # Análise detalhada por dimensão
        st.markdown("#### 📊 Análise Detalhada por Dimensão")

        # Identificar pontos fortes e fracos
        scores_f2 = {
            "Desenvolvimento Técnico": score_dev,
            "Seleção de Soluções": score_sel,
            "Planejamento e Layout": score_plan,
            "Aspectos Ambientais/Sociais": score_amb_soc,
            "Estimativas e Riscos": score_est
        }

        pontos_fortes_f2 = [k for k, v in scores_f2.items() if v >= 80]
        pontos_atenção_f2 = [k for k, v in scores_f2.items() if 60 <= v < 80]
        pontos_críticos_f2 = [k for k, v in scores_f2.items() if v < 60]

        col_analise1, col_analise2, col_analise3 = st.columns(3)

        with col_analise1:
            if pontos_fortes_f2:
                st.markdown("**🟢 Pontos Fortes**")
                for ponto in pontos_fortes_f2:
                    st.markdown(f"✅ {ponto}")
            else:
                st.markdown("**🟢 Pontos Fortes**")
                st.markdown("_Nenhum identificado_")

        with col_analise2:
            if pontos_atenção_f2:
                st.markdown("**🟡 Necessita Atenção**")
                for ponto in pontos_atenção_f2:
                    st.markdown(f"⚠️ {ponto}")
            else:
                st.markdown("**🟡 Necessita Atenção**")
                st.markdown("_Nenhum identificado_")

        with col_analise3:
            if pontos_críticos_f2:
                st.markdown("**🔴 Pontos Críticos**")
                for ponto in pontos_críticos_f2:
                    st.markdown(f"❌ {ponto}")
            else:
                st.markdown("**🔴 Pontos Críticos**")
                st.markdown("_Nenhum identificado_")

        # Comparação com FELKLA-1 (se disponível)
        st.markdown("#### 📈 Evolução do Projeto")

        # Aqui você pode adicionar uma comparação se tiver os dados do FELKLA-1
        st.info("""
            💡 **Dica:** Compare os resultados com a avaliação FELKLA-1 para verificar a evolução do projeto.

            **Principais focos desta fase:**
            - Desenvolvimento técnico detalhado
            - Seleção definitiva de soluções
            - Planejamento de implementação
            """)

        # Próximos passos
        st.markdown("#### 🚀 Próximos Passos Recomendados")

        if score_final_f2 >= 80:
            st.info("""
                        1. **Finalizar especificações técnicas** detalhadas
                        2. **Preparar documentação** para FELKLA-3
                        3. **Confirmar contratos** com fornecedores selecionados
                        4. **Iniciar estudos** de engenharia de detalhe
                        """)
        elif score_final_f2 >= 60:
            st.warning("""
                        1. **Aprofundar desenvolvimento** nas áreas críticas
                        2. **Revisar critérios** de seleção de soluções
                        3. **Melhorar integração** com operações existentes
                        4. **Reavaliar** após implementação das melhorias
                        """)
        else:
            st.error("""
                        1. **Revisar alternativas** técnicas propostas
                        2. **Reavaliar viabilidade** das soluções selecionadas
                        3. **Considerar retorno** ao FELKLA-1 para revisão
                        4. **Buscar suporte técnico** especializado
                        """)

        # Resumo executivo (AQUI COMEÇA A CORREÇÃO)
        st.markdown("#### 📋 Resumo Executivo")

        # Definir cores do resumo baseado no score
        resumo_color = "#d4edda" if score_final_f2 >= 80 else "#fff3cd" if score_final_f2 >= 60 else "#f8d7da"
        resumo_border = "#006837" if score_final_f2 >= 80 else "#ffc107" if score_final_f2 >= 60 else "#dc3545"

        st.markdown(f"""
                    <div style="background: {resumo_color}; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid {resumo_border}; margin: 1rem 0;">
                        <h4 style="margin-top: 0;">📊 Score Final: {score_final_f2:.1f}%</h4>
                        <p><strong>Melhor dimensão:</strong> {max(scores_f2, key=scores_f2.get)} ({max(scores_f2.values()):.1f}%)</p>
                        <p><strong>Dimensão crítica:</strong> {min(scores_f2, key=scores_f2.get)} ({min(scores_f2.values()):.1f}%)</p>
                        <p><strong>Questões respondidas:</strong> {len(respostas_preenchidas_f2)}/{len(todas_respostas_f2)}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Download do Relatório FELKLA-2
        st.markdown("---")

        # Verificar se campos obrigatórios estão preenchidos
        campos_obrigatorios_preenchidos = bool(nome_projeto and nome_avaliador and data_avaliacao and area_responsavel)

        if campos_obrigatorios_preenchidos:
            # Gerar relatório em texto
            relatorio_texto = f"""
        RELATÓRIO DE AVALIAÇÃO FELKLA-2
        =====================================

        IDENTIFICAÇÃO DO PROJETO:
        - Nome do Projeto: {nome_projeto}
        - Avaliador: {nome_avaliador}
        - Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}
        - Área Responsável: {area_responsavel}
        {f'- Código do Projeto: {codigo_projeto}' if codigo_projeto else ''}

        RESULTADO DA AVALIAÇÃO:
        - Score Final: {score_final_f2:.1f}%
        - Status: {'APROVADO' if score_final_f2 >= 80 else 'ATENÇÃO' if score_final_f2 >= 60 else 'NÃO APROVADO'}
        - Questões Respondidas: {len(respostas_preenchidas_f2)}/{len(todas_respostas_f2)}

        DETALHAMENTO POR DIMENSÃO:
        - Desenvolvimento Técnico: {score_dev:.1f}%
        - Seleção de Soluções: {score_sel:.1f}%
        - Planejamento e Layout: {score_plan:.1f}%
        - Aspectos Ambientais/Sociais: {score_amb_soc:.1f}%
        - Estimativas e Riscos: {score_est:.1f}%

        ANÁLISE:
        - Pontos Fortes: {', '.join(pontos_fortes_f2) if pontos_fortes_f2 else 'Nenhum identificado'}
        - Pontos de Atenção: {', '.join(pontos_atenção_f2) if pontos_atenção_f2 else 'Nenhum identificado'}
        - Pontos Críticos: {', '.join(pontos_críticos_f2) if pontos_críticos_f2 else 'Nenhum identificado'}

        PRÓXIMOS PASSOS:
        {'- Prosseguir para FELKLA-3' if score_final_f2 >= 80 else '- Aprofundar desenvolvimento técnico' if score_final_f2 >= 60 else '- Revisar alternativas técnicas propostas'}

        Relatório gerado automaticamente pela Metodologia FELKLA - Klabin
        Data de geração: {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}
                    """

            try:
                # Gerar PDF
                nome_arquivo = f"Relatorio_FELKLA-2_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.pdf"
                pdf_bytes = gerar_pdf_relatorio(relatorio_texto, nome_arquivo)

                st.markdown("#### 📥 Download do Relatório")
                col_download1, col_download2 = st.columns(2)

                with col_download1:
                    st.download_button(
                        label="📄 Download Relatório FELKLA-2 (.pdf)",
                        data=pdf_bytes,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )

                with col_download2:
                    st.button("📧 Enviar por Email", help="Funcionalidade em desenvolvimento")

            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
                # Fallback para TXT
                st.download_button(
                    label="📄 Download Relatório FELKLA-2 (.txt)",
                    data=relatorio_texto,
                    file_name=f"Relatorio_FELKLA-2_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.txt",
                    mime="text/plain"
                )
        else:
            st.info(
                "💡 **Dica:** Preencha as informações do projeto no topo da página para habilitar o download do relatório.")

with aba3:
    # Header da aba com informações
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">✅ QUESTIONÁRIO FELKLA-3</h2>
        <p style="color: #2d5016; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            <strong>Objetivo:</strong> Definição final e preparação para execução do projeto
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Indicador de progresso
    st.markdown("### 📊 Progresso do Questionário")
    progress_placeholder_3 = st.empty()


    # Função para contar respostas preenchidas FELKLA-3
    def contar_respostas_aba3():
        respostas = [q11_f3, q12_f3, q13_f3, q14_f3, q15_f3, q21_f3, q22_f3, q23_f3, q24_f3, q25_f3,
                     q31_f3, q32_f3, q33_f3, q34_f3, q35_f3, q41_f3, q42_f3, q43_f3, q44_f3, q45_f3,
                     q51_f3, q52_f3, q53_f3, q54_f3, q55_f3]
        preenchidas = len([r for r in respostas if r is not None])
        return preenchidas, len(respostas)


    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🔧 ENGENHARIA E ESPECIFICAÇÕES
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 35%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q11_f3 = st.selectbox(
            '**1.1** Engenharia de detalhe foi completada conforme escopo?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q11',
            help="Avalie se a engenharia de detalhe está completa e adequada"
        )

        q12_f3 = st.selectbox(
            '**1.2** Especificações técnicas finais foram aprovadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q12',
            help="Verifique se as especificações técnicas estão aprovadas"
        )

        q13_f3 = st.selectbox(
            '**1.3** Documentação técnica está completa e validada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q13',
            help="Avalie a completude e validação da documentação técnica"
        )

        q14_f3 = st.selectbox(
            '**1.4** Interfaces técnicas foram totalmente definidas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q14',
            help="Verifique se todas as interfaces técnicas estão definidas"
        )

        q15_f3 = st.selectbox(
            '**1.5** Testes e validações necessários foram planejados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q15',
            help="Avalie o planejamento de testes e validações"
        )

    with col2:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🤝 CONTRATAÇÃO E SUPRIMENTOS
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 25%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q21_f3 = st.selectbox(
            '**2.1** Estratégia de contratação foi definida e aprovada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q21',
            help="Verifique se a estratégia de contratação está definida"
        )

        q22_f3 = st.selectbox(
            '**2.2** Principais contratos foram negociados ou estão em fase final?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q22',
            help="Avalie o status das negociações contratuais"
        )

        q23_f3 = st.selectbox(
            '**2.3** Fornecedores críticos foram selecionados e qualificados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q23',
            help="Verifique a seleção e qualificação de fornecedores críticos"
        )

        q24_f3 = st.selectbox(
            '**2.4** Plano de suprimentos foi elaborado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q24',
            help="Avalie se o plano de suprimentos está elaborado"
        )

        q25_f3 = st.selectbox(
            '**2.5** Garantias e seguros foram definidos?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q25',
            help="Verifique se garantias e seguros estão definidos"
        )

    # Divisor visual personalizado
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                📋 LICENCIAMENTO E CONFORMIDADE
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 20%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q31_f3 = st.selectbox(
            '**3.1** Todas as licenças necessárias foram obtidas ou estão em processo final?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q31',
            help="Avalie o status das licenças necessárias"
        )

        q32_f3 = st.selectbox(
            '**3.2** Conformidade regulatória foi verificada e documentada?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q32',
            help="Verifique se a conformidade regulatória está documentada"
        )

        q33_f3 = st.selectbox(
            '**3.3** Certificações requeridas foram obtidas ou planejadas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q33',
            help="Avalie o status das certificações necessárias"
        )

        q34_f3 = st.selectbox(
            '**3.4** Aprovações internas necessárias foram obtidas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q34',
            help="Verifique se aprovações internas foram obtidas"
        )

        q35_f3 = st.selectbox(
            '**3.5** Condicionantes legais foram atendidas?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q35',
            help="Avalie se condicionantes legais foram atendidas"
        )

    with col4:
        st.markdown("""
        <div class="question-section">
            <h3 style="color: #006837; margin-bottom: 1rem;">
                🚀 PLANOS DE EXECUÇÃO
                <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 15%</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        q41_f3 = st.selectbox(
            '**4.1** Plano de execução detalhado foi elaborado e aprovado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q41',
            help="Verifique se o plano de execução está detalhado e aprovado"
        )

        q42_f3 = st.selectbox(
            '**4.2** Cronograma executivo está finalizado com recursos alocados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q42',
            help="Avalie se o cronograma executivo está finalizado"
        )

        q43_f3 = st.selectbox(
            '**4.3** Planos de qualidade, segurança e meio ambiente foram desenvolvidos?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q43',
            help="Verifique se planos de QSMS foram desenvolvidos"
        )

        q44_f3 = st.selectbox(
            '**4.4** Estratégia de comissionamento/start-up foi definida?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q44',
            help="Avalie se a estratégia de comissionamento está definida"
        )

        q45_f3 = st.selectbox(
            '**4.5** Plano de gestão de mudanças foi elaborado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q45',
            help="Verifique se o plano de gestão de mudanças existe"
        )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="question-section">
        <h3 style="color: #006837; margin-bottom: 1rem;">
            ⚙️ CONTROLES E RISCOS
            <span style="background: #006837; color: white; padding: 0.2rem 0.5rem; 
                  border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">PESO 5%</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col5, col6, col7 = st.columns([1, 1, 1])

    with col5:
        q51_f3 = st.selectbox(
            '**5.1** Sistema de controle do projeto foi estabelecido?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q51',
            help="Avalie se o sistema de controle está estabelecido"
        )

        q52_f3 = st.selectbox(
            '**5.2** Planos de contingência para riscos críticos foram finalizados?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q52',
            help="Verifique se planos de contingência estão finalizados"
        )

    with col6:
        q53_f3 = st.selectbox(
            '**5.3** Estrutura de governança do projeto foi definida?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q53',
            help="Avalie se a estrutura de governança está definida"
        )

        q54_f3 = st.selectbox(
            '**5.4** Critérios de aceitação foram estabelecidos?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q54',
            help="Verifique se critérios de aceitação estão estabelecidos"
        )

    with col7:
        q55_f3 = st.selectbox(
            '**5.5** Plano de encerramento do projeto foi elaborado?',
            ('Excelente', 'Bom', 'Regular', 'Inadequado', 'Não iniciado'),
            index=None,
            key='felkla3_q55',
            help="Avalie se o plano de encerramento foi elaborado"
        )

    # Atualizar progresso
    preenchidas_3, total_3 = contar_respostas_aba3()
    progress_percentage_3 = preenchidas_3 / total_3

    with progress_placeholder_3:
        st.progress(progress_percentage_3,
                    text=f"Progresso: {preenchidas_3}/{total_3} questões respondidas ({progress_percentage_3:.1%})")

        if preenchidas_3 < total_3:
            st.info(f"💡 **Dica:** Responda todas as {total_3} questões para obter uma avaliação completa!")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    # Seção de resultados melhorada FELKLA-3
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f8f0 0%, #ffffff 100%); 
                padding: 1.5rem; border-radius: 10px; margin: 2rem 0; 
                border-left: 5px solid #006837;">
        <h2 style="color: #006837; margin: 0;">📊 RELATÓRIO FELKLA-3</h2>
        <p style="color: #2d5016; margin: 0.5rem 0; font-size: 1.1rem;">
            Análise final de prontidão para execução do projeto
        </p>
        <div style="margin-top: 1rem; color: #2d5016;">
            <p style="margin: 0.3rem 0;"><strong>Projeto:</strong> {nome_projeto or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Avaliador:</strong> {nome_avaliador or 'Não informado'}</p>
            <p style="margin: 0.3rem 0;"><strong>Data:</strong> {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}</p>
            <p style="margin: 0.3rem 0;"><strong>Área:</strong> {area_responsavel or 'Não informada'}</p>
            {f'<p style="margin: 0.3rem 0;"><strong>Código:</strong> {codigo_projeto}</p>' if codigo_projeto else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Verificar se todas as questões foram respondidas
    todas_respostas_f3 = [q11_f3, q12_f3, q13_f3, q14_f3, q15_f3, q21_f3, q22_f3, q23_f3, q24_f3, q25_f3,
                          q31_f3, q32_f3, q33_f3, q34_f3, q35_f3, q41_f3, q42_f3, q43_f3, q44_f3, q45_f3,
                          q51_f3, q52_f3, q53_f3, q54_f3, q55_f3]

    respostas_preenchidas_f3 = [r for r in todas_respostas_f3 if r is not None]

    # Inicializar variáveis
    calcular_resultado_f3 = False

    if len(respostas_preenchidas_f3) == 0:
        st.info("🔍 **Responda as questões acima para gerar o resultado da avaliação FELKLA-3**")

    elif len(respostas_preenchidas_f3) < len(todas_respostas_f3):
        col_aviso1, col_aviso2 = st.columns([2, 1])
        with col_aviso1:
            st.warning(
                f"⚠️ **Atenção:** {len(todas_respostas_f3) - len(respostas_preenchidas_f3)} questões ainda não foram respondidas. Para uma avaliação completa, responda todas as questões.")
        with col_aviso2:
            calcular_resultado_f3 = st.button("📊 Calcular Resultado Parcial FELKLA-3", type="secondary")

    else:
        # Todas as questões respondidas
        calcular_resultado_f3 = st.button("🚀 Calcular Resultado Completo FELKLA-3", type="primary")

    if calcular_resultado_f3:
        # Cálculos dos scores FELKLA-3
        # Engenharia e Especificações (35%)
        eng_esp = [q11_f3, q12_f3, q13_f3, q14_f3, q15_f3]
        pontos_eng = sum([calcular_pontuacao(resp) for resp in eng_esp if resp is not None])
        max_pontos_eng = len([resp for resp in eng_esp if resp is not None]) * 5
        score_eng = (pontos_eng / max_pontos_eng * 100) if max_pontos_eng > 0 else 0

        # Contratação e Suprimentos (25%)
        cont_sup = [q21_f3, q22_f3, q23_f3, q24_f3, q25_f3]
        pontos_cont = sum([calcular_pontuacao(resp) for resp in cont_sup if resp is not None])
        max_pontos_cont = len([resp for resp in cont_sup if resp is not None]) * 5
        score_cont = (pontos_cont / max_pontos_cont * 100) if max_pontos_cont > 0 else 0

        # Licenciamento e Conformidade (20%)
        lic_conf = [q31_f3, q32_f3, q33_f3, q34_f3, q35_f3]
        pontos_lic = sum([calcular_pontuacao(resp) for resp in lic_conf if resp is not None])
        max_pontos_lic = len([resp for resp in lic_conf if resp is not None]) * 5
        score_lic = (pontos_lic / max_pontos_lic * 100) if max_pontos_lic > 0 else 0

        # Planos de Execução (15%)
        plan_exec = [q41_f3, q42_f3, q43_f3, q44_f3, q45_f3]
        pontos_plan_exec = sum([calcular_pontuacao(resp) for resp in plan_exec if resp is not None])
        max_pontos_plan_exec = len([resp for resp in plan_exec if resp is not None]) * 5
        score_plan_exec = (pontos_plan_exec / max_pontos_plan_exec * 100) if max_pontos_plan_exec > 0 else 0

        # Controles e Riscos (5%)
        cont_risco = [q51_f3, q52_f3, q53_f3, q54_f3, q55_f3]
        pontos_cont_risco = sum([calcular_pontuacao(resp) for resp in cont_risco if resp is not None])
        max_pontos_cont_risco = len([resp for resp in cont_risco if resp is not None]) * 5
        score_cont_risco = (pontos_cont_risco / max_pontos_cont_risco * 100) if max_pontos_cont_risco > 0 else 0

        # Score Final Ponderado
        score_final_f3 = (score_eng * 0.35 + score_cont * 0.25 + score_lic * 0.20 +
                          score_plan_exec * 0.15 + score_cont_risco * 0.05)

        # Dashboard de resultados
        st.markdown("### 📈 Dashboard de Resultados FELKLA-3")

        # Métricas principais em cards
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

        with col_m1:
            delta_eng = "🎯" if score_eng >= 80 else "⚠️" if score_eng >= 60 else "❌"
            st.metric(
                "Engenharia e Especificações",
                f"{score_eng:.1f}%",
                delta=f"Peso: 35% {delta_eng}"
            )

        with col_m2:
            delta_cont = "🎯" if score_cont >= 80 else "⚠️" if score_cont >= 60 else "❌"
            st.metric(
                "Contratação e Suprimentos",
                f"{score_cont:.1f}%",
                delta=f"Peso: 25% {delta_cont}"
            )

        with col_m3:
            delta_lic = "🎯" if score_lic >= 80 else "⚠️" if score_lic >= 60 else "❌"
            st.metric(
                "Licenciamento e Conformidade",
                f"{score_lic:.1f}%",
                delta=f"Peso: 20% {delta_lic}"
            )

        with col_m4:
            delta_plan_exec = "🎯" if score_plan_exec >= 80 else "⚠️" if score_plan_exec >= 60 else "❌"
            st.metric(
                "Planos de Execução",
                f"{score_plan_exec:.1f}%",
                delta=f"Peso: 15% {delta_plan_exec}"
            )

        with col_m5:
            delta_cont_risco = "🎯" if score_cont_risco >= 80 else "⚠️" if score_cont_risco >= 60 else "❌"
            st.metric(
                "Controles e Riscos",
                f"{score_cont_risco:.1f}%",
                delta=f"Peso: 5% {delta_cont_risco}"
            )

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        # Score final destacado
        col_score, col_interpretation = st.columns([1, 2])

        with col_score:
            if score_final_f3 >= 80:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #006837; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #006837; margin: 0; font-size: 3rem;">{score_final_f3:.1f}%</h1>
                        <h3 style="color: #155724; margin: 0.5rem 0;">✅ PRONTO PARA EXECUÇÃO</h3>
                        <p style="color: #155724; margin: 0;">Projeto aprovado para implementação</p>
                    </div>
                    """, unsafe_allow_html=True)
            elif score_final_f3 >= 60:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #ffc107; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #856404; margin: 0; font-size: 3rem;">{score_final_f3:.1f}%</h1>
                        <h3 style="color: #856404; margin: 0.5rem 0;">⚠️ ATENÇÃO</h3>
                        <p style="color: #856404; margin: 0;">Projeto necessita melhorias</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; 
                                border: 3px solid #dc3545; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h1 style="color: #721c24; margin: 0; font-size: 3rem;">{score_final_f3:.1f}%</h1>
                        <h3 style="color: #721c24; margin: 0.5rem 0;">❌ NÃO APROVADO</h3>
                        <p style="color: #721c24; margin: 0;">Projeto não pronto para execução</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_interpretation:
            st.markdown("#### 🎯 Interpretação dos Resultados")

            if score_final_f3 >= 80:
                st.success("""
                    **Excelente! Projeto pronto para execução**

                    ✅ **Recomendações:**
                    - Iniciar fase de implementação
                    - Ativar estrutura de governança
                    - Executar planos de comunicação
                    """)
            elif score_final_f3 >= 60:
                st.warning("""
                    **Projeto viável com ajustes necessários**

                    ⚠️ **Ações recomendadas:**
                    - Finalizar documentação pendente
                    - Completar contratações críticas
                    - Resolver pendências de licenciamento
                    """)
            else:
                st.error("""
                    **Projeto não pronto para execução**

                    ❌ **Ações necessárias:**
                    - Revisar engenharia de detalhe
                    - Finalizar contratos principais
                    - Resolver questões regulatórias
                    """)

        # Análise detalhada por dimensão
        st.markdown("#### 📊 Análise Detalhada por Dimensão")

        # Identificar pontos fortes e fracos
        scores_f3 = {
            "Engenharia e Especificações": score_eng,
            "Contratação e Suprimentos": score_cont,
            "Licenciamento e Conformidade": score_lic,
            "Planos de Execução": score_plan_exec,
            "Controles e Riscos": score_cont_risco
        }

        pontos_fortes_f3 = [k for k, v in scores_f3.items() if v >= 80]
        pontos_atenção_f3 = [k for k, v in scores_f3.items() if 60 <= v < 80]
        pontos_críticos_f3 = [k for k, v in scores_f3.items() if v < 60]

        col_analise1, col_analise2, col_analise3 = st.columns(3)

        with col_analise1:
            if pontos_fortes_f3:
                st.markdown("**🟢 Pontos Fortes**")
                for ponto in pontos_fortes_f3:
                    st.markdown(f"✅ {ponto}")
            else:
                st.markdown("**🟢 Pontos Fortes**")
                st.markdown("_Nenhum identificado_")

        with col_analise2:
            if pontos_atenção_f3:
                st.markdown("**🟡 Necessita Atenção**")
                for ponto in pontos_atenção_f3:
                    st.markdown(f"⚠️ {ponto}")
            else:
                st.markdown("**🟡 Necessita Atenção**")
                st.markdown("_Nenhum identificado_")

        with col_analise3:
            if pontos_críticos_f3:
                st.markdown("**🔴 Pontos Críticos**")
                for ponto in pontos_críticos_f3:
                    st.markdown(f"❌ {ponto}")
            else:
                st.markdown("**🔴 Pontos Críticos**")
                st.markdown("_Nenhum identificado_")

        # Checklist de prontidão para execução
        st.markdown("#### ✅ Checklist de Prontidão para Execução")

        checklist_items = [
            ("Engenharia de detalhe completa", score_eng >= 80),
            ("Contratos principais assinados", score_cont >= 80),
            ("Licenças obtidas", score_lic >= 80),
            ("Planos de execução aprovados", score_plan_exec >= 80),
            ("Sistema de controle estabelecido", score_cont_risco >= 80)
        ]

        col_check1, col_check2 = st.columns(2)

        for i, (item, status) in enumerate(checklist_items):
            col = col_check1 if i % 2 == 0 else col_check2
            with col:
                icon = "✅" if status else "❌"
                color = "#155724" if status else "#721c24"
                st.markdown(f"<span style='color: {color};'>{icon} {item}</span>", unsafe_allow_html=True)

        # Próximos passos
        st.markdown("#### 🚀 Próximos Passos Recomendados")

        if score_final_f3 >= 80:
            st.info("""
                1. **Kick-off oficial** do projeto de execução
                2. **Ativar estrutura** de governança e controle
                3. **Mobilizar equipes** e recursos alocados
                4. **Executar planos** de comunicação e engajamento
                5. **Iniciar monitoramento** de marcos e entregas
                """)
        elif score_final_f3 >= 60:
            st.warning("""
                1. **Finalizar pendências** identificadas nas áreas críticas
                2. **Completar documentação** técnica e contratual
                3. **Resolver questões** de licenciamento pendentes
                4. **Reavaliar prontidão** após correções
                5. **Planejar cronograma** considerando ajustes
                """)
        else:
            st.error("""
                1. **Revisar completamente** engenharia e especificações
                2. **Renegociar contratos** ou buscar novos fornecedores
                3. **Resolver questões** regulatórias e de conformidade
                4. **Considerar retorno** ao FELKLA-2 para revisão
                5. **Reavaliar viabilidade** do cronograma proposto
                """)

        # Resumo executivo final
        st.markdown("#### 📋 Resumo Executivo Final")

        resumo_color = "#d4edda" if score_final_f3 >= 80 else "#fff3cd" if score_final_f3 >= 60 else "#f8d7da"
        resumo_border = "#006837" if score_final_f3 >= 80 else "#ffc107" if score_final_f3 >= 60 else "#dc3545"

        prontidao_status = "PRONTO" if score_final_f3 >= 80 else "PENDENTE" if score_final_f3 >= 60 else "NÃO PRONTO"

        st.markdown(f"""
                    <div style="background: {resumo_color}; padding: 1.5rem; border-radius: 10px; 
                                border-left: 4px solid {resumo_border}; margin: 1rem 0;">
                        <h4 style="margin-top: 0;">🎯 Status Final: {prontidao_status} PARA EXECUÇÃO</h4>
                        <p><strong>Score FELKLA-3:</strong> {score_final_f3:.1f}%</p>
                        <p><strong>Dimensão mais forte:</strong> {max(scores_f3, key=scores_f3.get)} ({max(scores_f3.values()):.1f}%)</p>
                        <p><strong>Dimensão crítica:</strong> {min(scores_f3, key=scores_f3.get)} ({min(scores_f3.values()):.1f}%)</p>
                        <p><strong>Questões respondidas:</strong> {len(respostas_preenchidas_f3)}/{len(todas_respostas_f3)}</p>
                        <p><strong>Itens do checklist aprovados:</strong> {sum(1 for _, status in checklist_items if status)}/{len(checklist_items)}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # ADICIONE ESTA PARTE AQUI ↓↓↓

        # Download do Relatório FELKLA-3
        st.markdown("---")

        # Verificar se campos obrigatórios estão preenchidos
        campos_obrigatorios_preenchidos = bool(nome_projeto and nome_avaliador and data_avaliacao and area_responsavel)

        if campos_obrigatorios_preenchidos:
            # Gerar relatório em texto (mesmo conteúdo que já existe)
            relatorio_texto = f"""
        RELATÓRIO DE AVALIAÇÃO FELKLA-3
        =====================================

        IDENTIFICAÇÃO DO PROJETO:
        - Nome do Projeto: {nome_projeto}
        - Avaliador: {nome_avaliador}
        - Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}
        - Área Responsável: {area_responsavel}
        {f'- Código do Projeto: {codigo_projeto}' if codigo_projeto else ''}

        RESULTADO DA AVALIAÇÃO:
        - Score Final: {score_final_f3:.1f}%
        - Status: {'PRONTO PARA EXECUÇÃO' if score_final_f3 >= 80 else 'ATENÇÃO' if score_final_f3 >= 60 else 'NÃO PRONTO'}
        - Questões Respondidas: {len(respostas_preenchidas_f3)}/{len(todas_respostas_f3)}

        DETALHAMENTO POR DIMENSÃO:
        - Engenharia e Especificações: {score_eng:.1f}%
        - Contratação e Suprimentos: {score_cont:.1f}%
        - Licenciamento e Conformidade: {score_lic:.1f}%
        - Planos de Execução: {score_plan_exec:.1f}%
        - Controles e Riscos: {score_cont_risco:.1f}%

        ANÁLISE:
        - Pontos Fortes: {', '.join(pontos_fortes_f3) if pontos_fortes_f3 else 'Nenhum identificado'}
        - Pontos de Atenção: {', '.join(pontos_atenção_f3) if pontos_atenção_f3 else 'Nenhum identificado'}
        - Pontos Críticos: {', '.join(pontos_críticos_f3) if pontos_críticos_f3 else 'Nenhum identificado'}

        CHECKLIST DE PRONTIDÃO:
        - Engenharia de detalhe completa: {'✅' if checklist_items[0][1] else '❌'}
        - Contratos principais assinados: {'✅' if checklist_items[1][1] else '❌'}
        - Licenças obtidas: {'✅' if checklist_items[2][1] else '❌'}
        - Planos de execução aprovados: {'✅' if checklist_items[3][1] else '❌'}
        - Sistema de controle estabelecido: {'✅' if checklist_items[4][1] else '❌'}
        - Itens aprovados: {sum(1 for _, status in checklist_items if status)}/{len(checklist_items)}

        PRÓXIMOS PASSOS:
        {'- Iniciar fase de implementação' if score_final_f3 >= 80 else '- Finalizar pendências identificadas' if score_final_f3 >= 60 else '- Revisar completamente engenharia e especificações'}

        CONCLUSÃO METODOLOGIA FELKLA:
        {'✅ PROJETO APROVADO - Metodologia FELKLA concluída com sucesso' if score_final_f3 >= 80 else '⚠️ PROJETO COM PENDÊNCIAS - Necessita ajustes antes da execução' if score_final_f3 >= 60 else '❌ PROJETO NÃO APROVADO - Não recomendado para execução'}

        Relatório gerado automaticamente pela Metodologia FELKLA - Klabin
        Data de geração: {data_avaliacao.strftime('%d/%m/%Y') if data_avaliacao else 'Não informada'}
                    """

            try:
                # Gerar PDF
                nome_arquivo = f"Relatorio_FELKLA-3_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.pdf"
                pdf_bytes = gerar_pdf_relatorio(relatorio_texto, nome_arquivo)

                st.markdown("#### 📥 Download do Relatório")
                col_download1, col_download2 = st.columns(2)

                with col_download1:
                    st.download_button(
                        label="📄 Download Relatório FELKLA-3 (.pdf)",
                        data=pdf_bytes,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )

                with col_download2:
                    st.button("📧 Enviar por Email", help="Funcionalidade em desenvolvimento")

            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
                # Fallback para TXT
                st.download_button(
                    label="📄 Download Relatório FELKLA-3 (.txt)",
                    data=relatorio_texto,
                    file_name=f"Relatorio_FELKLA-3_{nome_projeto.replace(' ', '_') if nome_projeto else 'Projeto'}_{data_avaliacao.strftime('%Y%m%d') if data_avaliacao else 'SemData'}.txt",
                    mime="text/plain"
                )
        else:
            st.info(
                "💡 **Dica:** Preencha as informações do projeto no topo da página para habilitar o download do relatório.")

        # Conclusão da metodologia FELKLA
        if score_final_f3 >= 80:
            st.balloons()
            st.success("""
                🎉 **Parabéns! O projeto completou com sucesso a metodologia FELKLA e está pronto para execução.**

                A metodologia FELKLA foi concluída com aprovação em todas as fases:
                - ✅ FELKLA-1: Avaliação de oportunidades
                - ✅ FELKLA-2: Seleção de alternativas  
                - ✅ FELKLA-3: Definição do projeto

                **O projeto pode prosseguir para a fase de implementação!**
                """)
