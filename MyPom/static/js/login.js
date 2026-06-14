const login_form = document.getElementById("login-form");
const title = document.getElementById("title");
const errorMensagem = document.getElementById("errorMessage");

login_form.addEventListener("submit", async (event) => {
	event.preventDefault();

	const formData = new FormData(login_form);
	const data = new URLSearchParams(formData);

	const response = await fetch("/token", {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
		body: data,
	});
	if (!response.ok) {
		errorMensagem.innerText =
			"Usuário ou senha incorretos. Verifique os dados.";
		return;
	}
	const result = await response.json();

	localStorage.setItem("access_token", result.access_token);

	alert("Login realizado com sucesso!");
	window.location.replace("/");
});

title.addEventListener("click", async (e) => {
	e.preventDefault();

	window.location.href = "/";
});
