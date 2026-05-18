const register_form = document.getElementById("register-form");
const confirm_password = document.getElementById("confirm-password");

register_form.addEventListener("submit", async (e) => {
	e.preventDefault();

	const form = new FormData(register_form);
	const data = Object.fromEntries(form);

	if (data.password !== confirm_password) {
		alert("As senhas não coincidem!");
		return;
	}
	try {
		const response = await fetch("/user/createUser", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				username: data.username,
				email: data.email,
				password: data.password,
			}),
		});
		if (response.ok) {
			alert("Usuário criado com sucesso.");
			window.location.href = "/page/login";
		} else {
			const errData = await response.json();
			alert(`Erro: ${errData.detail.msg || "Erro ao cadastrar."}`);
		}
	} catch (error) {
		console.error("Erro na requisição:", error);
	}
});
