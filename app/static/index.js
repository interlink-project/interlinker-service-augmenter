function deleteAnotacion(anotacionId, anotacionIdCode) {
  fetch("/delete-anotacion", {
    method: "POST",
    body: JSON.stringify({ anotacionId: anotacionId }),
  }).then((_res) => {
    //Elimino la anotacion de la base de ElasticSearch

    fetch(
      "http://127.0.0.1:80/annotations/" + anotacionIdCode,
      {
        method: "DELETE",
      }
    ).then(function (data) {
      console.log(data);
      //Reload the page after GET
      window.location.href = "/";
    });
  });
}

function deleteDescription(descriptionId, descriptionIdCode) {
  fetch("/delete-description", {
    method: "POST",
    body: JSON.stringify({ descriptionId: descriptionId }),
  }).then((_res) => {
    //Elimino todas las descripciones relacionadas:

    fetch(
      "http://127.0.0.1:80/annotations/" + descriptionIdCode,
      {
        method: "DELETE",
      }
    ).then(function (data) {
      console.log(data);
      //Reload the page after GET
      window.location.href = "/";
    });
  });
}

window.addEventListener("pageshow", function (event) {
  var historyTraversal =
    event.persisted ||
    (typeof window.performance != "undefined" &&
      window.performance.navigation.type === 2);
  if (historyTraversal) {
    // Handle page restore.
    window.location.reload();
  }
});
