const clear_data = document.getElementById("btn-clear-data");
const focus_time = document.getElementById("focus-time");
const btn_time = document.getElementById("btn-pomo-time");

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
