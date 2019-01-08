<?php
session_start();
header("Content-type:text/html;charset=utf-8");
$link = mysqli_connect('localhost','root','xm19961107','HanFu');  //链接数据库
 mysqli_set_charset($link ,'utf8'); //设定字符集 

$name=$_POST['name'];

$pwd=$_POST['pwd'];

$yzm=$_POST['yzm'];

    if($name==''){
        echo "<script>alert('请输入用户名');location='" . $_SERVER['HTTP_REFERER'] . "'</script>";
        exit;
    }
    if($pwd==''){

        echo "<script>alert('请输入密码');location='" . $_SERVER['HTTP_REFERER'] . "'</script>";
        exit;

    }

    if($yzm!=$_SESSION['VCODE']){

        echo"<script>alert('你的验证码不正确，请重新输入');location='".$_SERVER['HTTP_REFERER']. "'</script>";
        exit;

    }


    $sql_select="select id,username,password,status from user where username= $name";      //从数据库查询信息
    $stmt=mysqli_prepare($link,$sql_select);
    mysqli_stmt_bind_param($stmt,'s',$name);
    mysqli_stmt_execute($stmt);
    $result=mysqli_stmt_get_result($stmt);
    $row=mysqli_fetch_assoc($result);

    if($row){

        if($pwd !=$row['password'] || $name !=$row['username']){

            echo "<script>alert('密码错误，请重新输入');location.href='login.html'</script>";
            exit;
        }
        else{
            echo "<script>alert('登录成功');location.href='tech-index.html'</script>";
        }
        /*不同身份登陆
        else{
            $_SESSION['username']=$row['username'];
            $_SESSION['id']=$row['id'];
            if($row['status']=='1'){
                echo "<script>alert('登录成功');location.href='../manager-pages/manager-index.html'</script>";
            }
            echo "<script>alert('登录成功');location.href='../user-pages/user-index.html'</script>";
        }
        */

    }else{
        echo "<script>alert('您输入的用户名不存在');location.href='login.html'</script>";
        exit;
    };