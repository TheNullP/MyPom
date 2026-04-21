const clear_data = document.getElementById("btn-clear-data");

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
      throw alert(f`Erro inesperado ao tentar excluir Banco de dados.${error}`);
    }
  }
});
