<?php

$Nome = $Email = $Senha = $confSenha = $Faculdade = $Curso = $Periodo = '';
$NomeErro = $EmailErro = $SenhaErro = $confSenhaErro = $MensagemErro = '';

// Verifica se o formulário foi enviado
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $Nome = $_POST['nome'];
    $Email = $_POST['email'];
    $Senha = $_POST['senha'];
    $confSenha = $_POST['confsenha'];
    $Faculdade = $_POST['faculdade'];
    $Curso = $_POST['curso'];
    $Periodo = $_POST['periodo'];

    // Validação dos campos
    if (empty($Nome)) {
        $NomeErro = 'Insira seu nome.';
    }
    if (empty($Email)) {
        $EmailErro = 'Insira seu email.';
    } elseif (!filter_var($Email, FILTER_VALIDATE_EMAIL)) {
        $EmailErro = 'Formato de email inválido.';
    }
    if (empty($Senha)) {
        $SenhaErro = 'Insira sua senha.';
    }
    if ($Senha != $confSenha) {
        $confSenhaErro = 'As senhas não coincidem.';
    }

    // Se não houver erros, realiza o cadastro
    if (empty($NomeErro) && empty($EmailErro) && empty($SenhaErro) && empty($confSenhaErro)) {

        $host = 'localhost';
        $banco = 'campuslink_integrado';
        $user = 'Feellype';
        $senha_banco = '13020101'; // Coloque a senha correta aqui

        // Conexão com o banco de dados
        $con = mysqli_connect($host, $user, $senha_banco, $banco);

        if (!$con) {
            die('Erro na conexão: ' . mysqli_connect_error());
        }

        // Prepara o SQL para evitar SQL Injection
        $sql = "INSERT INTO usuarios (Nome, Email, Senha, Faculdade, Curso, Periodo) VALUES (?, ?, ?, ?, ?, ?)";

        if ($stmt = mysqli_prepare($con, $sql)) {
            // Cria o hash da senha
            $SenhaHash = password_hash($Senha, PASSWORD_DEFAULT);

            // Associa os parâmetros
            mysqli_stmt_bind_param($stmt, 'ssssss', $Nome, $Email, $SenhaHash, $Faculdade, $Curso, $Periodo);

            // Executa o comando
            if (mysqli_stmt_execute($stmt)) {
                echo "Cadastro realizado com sucesso.";
            } else {
                echo "Erro ao realizar o cadastro.";
            }

            // Fecha o statement
            mysqli_stmt_close($stmt);
        } else {
            echo "Erro ao preparar a consulta: " . mysqli_error($con);
        }

        // Fecha a conexão com o banco de dados
        mysqli_close($con);
    }
}
?>
