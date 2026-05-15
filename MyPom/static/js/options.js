const clear_data = document.getElementById("btn-clear-data");
const focus_time = document.getElementById("focus-time");
const btn_time = document.getElementById("btn-pomo-time");
const user_name = document.getElementById("user-name");
const user_email = document.getElementById("user-email");
const user_initial = document.getElementById("user-initial");
const btn_logout = document.getElementById("btn-logout");

clear_data.addEventListener("click", async () => {
	const confirmed = confirm(
		"Tem certeza que deseja excluir seu banco de dados?(Ação irreversível).",
	);

	if (confirmed) {
		try {
			const response = await fetch("/options/clearDb", {
				method: "DELETE",
			});

			if (response.ok) {
				alert("Banco de dados deletao com sucesso.");
			} else {
				throw alert("Erro inesperado ao tentar excluir Banco de dados.");
			}
		} catch (error) {
			throw new Error(
				f`Erro inesperado ao tentar excluir Banco de dados: ${error}`,
			);
		}
	}
});

btn_time.addEventListener("click", async () => {
	const selectValue = focus_time.value;
	try {
		const response = await fetch("/options/updateFocus", {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ focus: parseInt(selectValue) }),
		});

		if (response.ok) {
			alert("Atualizado com sucesso.");
		}
	} catch (error) {
		throw new Error(`Error: ${error}`);
	}
});

document.addEventListener("DOMContentLoaded", async () => {
	const token = localStorage.getItem("access_token");
	try {
		const response = await fetch("/user/currentUser", {
			method: "GET",
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		if (response.ok) {
			const data = await response.json();

			user_name.innerHTML = data.username;
			user_email.innerHTML = data.email;
			user_initial.innerHTML = data.username[0];
			btn_logout.innerHTML = "Sair";
			btn_logout.style.color = "green";
		} else {
			user_name.innerHTML = "Não logado";
			btn_logout.innerHTML = "Entrar";
			btn_logout.style.color = "#ff2f00";
		}
	} catch (error) {
		throw new Error(`Error: ${error}`);
	}
});

btn_logout.addEventListener("click", async () => {
	const token = localStorage.getItem("access_token");
	try {
		const login = await fetch("/user/currentUser", {
			method: "GET",
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		if (login.ok) {
			localStorage.removeItem("access_token");
			window.location.reload();
			alert("Sessão encerrada com sucesso!");
		} else {
			window.location.href = "/page/login";
		}
	} catch (error) {}
});
