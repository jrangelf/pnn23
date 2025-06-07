function imprimirTabela() {
    // Seleciona a div com o conteúdo que você quer imprimir
    const conteudo = document.getElementById("print-section").innerHTML;

    // Cria uma nova janela (ou iframe) para imprimir
    const estilo = `
        <style>            
            body { 
             font-family: Arial, sans-serif; 
             padding: 10px;
              }
            
                         
           th, td { 
             border: 1px solid #333; 
             padding: 8px; 
             text-align: center; }
           
           th { 
             background-color: #f2f2f2; }
           
           p { font-size: 14px; }

        </style>
    `;        

    // Abre uma nova janela e insere o conteúdo + estilo
    const janela = window.open('', '_blank');
    const bootstrapCSS = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap @5.3.3/dist/css/bootstrap.min.css">'; // Nota: Há um espaço em 'bootstrap @5.3.3' que pode ser um erro de digitação
    janela.document.write('<html><head><title>PNN/23</title>');
    janela.document.write(bootstrapCSS);    
    janela.document.write(estilo);
    janela.document.write('</head><body>');
    janela.document.write(conteudo);
    janela.document.write('</body></html>');
    janela.document.close();

    // Chama a função de impressão
    //janela.print();
    janela.onload = () => janela.print();
}
function doDecimal() {
    //let valor = 0;             
    let valor = parseFloat(document.getElementById("valor").value.replace(/[^\d,]/g, '').replace(",", "."));        
}   

function formatarNumero(input) {
    // Remover todos os caracteres que não são dígitos ou vírgula
    let value = input.value.replace(/[^\d,]/g, '');
    // Formatar o número com separadores de milhar
    let valorFormatado = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    input.value = valorFormatado;
}
   
// Lógica de ativar/desativar required com base no checkbox
window.addEventListener('DOMContentLoaded', function () {
    const aplicarJurosCheckbox = document.getElementById('aplicar_juros');
    const dataInicioInput = document.getElementById('data_inicio');

    function atualizarObrigatoriedade() {
    if (aplicarJurosCheckbox.checked) {
        dataInicioInput.setAttribute('required', 'required');
    } else {
        dataInicioInput.removeAttribute('required');
    }
    }

    aplicarJurosCheckbox.addEventListener('change', atualizarObrigatoriedade);
    atualizarObrigatoriedade(); // executa ao carregar
});



// Validação dos campos no envio do formulário
document.getElementById('pnn23').addEventListener('submit', function (event) {
    // Lista de campos a validar
    const campos = [
    { id: 'atualizacao', nome: 'Data de atualização' },
    { id: 'data_inicio', nome: 'Data de início' },
    { id: 'data_atualizar', nome: 'Data do arbitramento' }
    ];

    let formularioValido = true;

    campos.forEach(campo => {
    const input = document.getElementById(campo.id);
    const valor = input.value;

    if (valor) {
        const [ano, mes] = valor.split('-');

        // Valida se o ano tem exatamente 4 dígitos
        if (!/^\d{4}$/.test(ano)) {
        alert(`O campo "${campo.nome}" deve conter um ano com exatamente 4 dígitos.`);
        input.focus();
        formularioValido = false;
        }

        // Verifica se o ano é menor que 1960 ou maior que o ano atual
        else if (parseInt(ano) < 1960 || parseInt(ano) > new Date().getFullYear()) {
            alert(`O campo "${campo.nome}" deve conter um ano entre 1960 e ${new Date().getFullYear()}.`);
            input.focus();
            formularioValido = false;
        }        
    }
    });

    

    // Se algum campo estiver inválido, cancela o envio
    if (!formularioValido) {
    event.preventDefault();
    }
});