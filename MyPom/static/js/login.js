const login_form = document.getElementById("login-form");
const title = document.getElementById("title");

login_form.addEventListener("submit", async (event) => {
	event.preventDefault();

	const formData = new FormData(login_form);
	const data = new URLSearchParams(formData);

	const response = await fetch("/token", {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
		body: data,
	});
	if (response.ok) {
		const result = await response.json();

		localStorage.setItem("access_token", result.access_token);

		alert("Login realizado com sucesso!");
		window.location.replace("/");
	} else {
		const error = await response.json();
		alert(`Erro: ${error.detail}`);
	}
});

title.addEventListener("click", async (e) => {
	e.preventDefault();

	window.location.href = "/";
});
