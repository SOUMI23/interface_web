document.getElementById("generateButton").addEventListener("click", async () => {
    const text = document.getElementById("inputText").value;
    const selectedTypes = Array.from(document.querySelectorAll("input[name='questionType']:checked"))
                               .map(checkbox => checkbox.value);

    if (!text.trim()) {
        alert("Veuillez entrer un texte.");
        return;
    }
    if (selectedTypes.length === 0) {
        alert("Veuillez sélectionner au moins un type de question.");
        return;
    }

    // Afficher la barre de chargement et la rendre visible
    document.getElementById("progressBarContainer").style.display = "block";
    let progress = 0;
    let progressBar = document.getElementById("progressBar");
    progressBar.style.width = progress + "%";

    // Augmenter progressivement la barre de progression pour simuler le chargement
    const interval = setInterval(() => {
        if (progress < 80) {  // Accélérer jusqu'à 80% (c'est juste un exemple)
            progress += 2;
            progressBar.style.width = progress + "%";
        }
    }, 100);

    const requestData = {
        text: text,
        question_types: selectedTypes
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/generate_questions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        // Masquer la barre de chargement une fois les questions générées
        clearInterval(interval);  // Arrêter l'intervalle
        progress = 100;
        progressBar.style.width = progress + "%"; // Finaliser la barre à 100%

        setTimeout(() => {
            document.getElementById("progressBarContainer").style.display = "none";  // Masquer après un délai
        }, 500);

        let outputDiv = document.getElementById("output");
        outputDiv.innerHTML = "<h3>Questions Générées :</h3>";

        if (result.generated_questions.length === 0) {
            outputDiv.innerHTML += "<p>Aucune question générée.</p>";
        } else {
            result.generated_questions.forEach(q => {
                outputDiv.innerHTML += `<p><strong>${q.type} :</strong> ${q.question}</p>`;
            });
        }

    } catch (error) {
        // Masquer la barre de chargement en cas d'erreur
        clearInterval(interval);
        document.getElementById("progressBarContainer").style.display = "none";  
        console.error("Erreur lors de la requête :", error);
        alert("Une erreur s'est produite lors de la génération des questions.");
    }
});
