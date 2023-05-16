//Falta cargar de nuevo cuando se tenga una consulta en memoria

function searchText(event) {
  if (event.type == "click") {
    event.preventDefault();

    textoBox = document.getElementById("searchBox");
    texto = textoBox.value;

    padministration = document.getElementById("padministration");
    padministrationSel = padministration.selectedOptions[0].label;

    if (padministration.selectedOptions[0].index == 0) {
      padministrationSel = "";
    }

    domain = document.getElementById("domain");
    domainSel = domain.selectedOptions[0].label;

    let page = event.target.getAttribute("page");
    if (page == null) {
      page = 1;
    }

    if (domain.selectedOptions[0].index == 0) {
      domainSel = "";
    }

    //window.location = '/?searchText=' + texto+'&padministration=' + padministrationSel+'&domain=' + domainSel;
    //recargarTabla();

    function addShow(data) {
      entries = Object.entries(data);
      descripcionesList = entries["0"][1];
      numeroReg = entries[1][1];

      $("#tablaDescriptions").empty();

      for (let dataItem of descripcionesList) {
        $("#tablaDescriptions").append(
          " <tr> <td> " +
            dataItem.padministration +
            " </td> <td> " +
            dataItem.title +
            " </td>  <td> " +
            dataItem.created +
            ' </td> <td> <i class="bi bi-box-arrow-in-right " style="width:100px;"></i> </td></tr>'
        );
      }

      $("#totalRegisters").text(numeroReg);

      $("#page").text("1");

      numeroPaginas = Math.ceil(numeroReg / 10);
      $("#pagesNumbers").text(numeroPaginas);

      textoBox = document.getElementById("searchBox");
      texto = textoBox.value;

      padministration = document.getElementById("padministration");
      padministrationSel = padministration.selectedOptions[0].label;

      if (padministration.selectedOptions[0].index == 0) {
        padministrationSel = "";
      }

      domain = document.getElementById("domain");
      domainSel = domain.selectedOptions[0].label;

      if (domain.selectedOptions[0].index == 0) {
        domainSel = "";
      }

      $("#paginador").empty();
      for (var j = 1; j < numeroPaginas + 1; j++) {
        //$('#paginador').append(" <li class='page-item'><a class='page-link' href='?page="+j+"&textoABuscar="+texto+"&padministration="+padministrationSel+"&domain="+domainSel+"'>"+j+"</a></li>");
        $("#paginador").append(
          " <li class='page-item'><a class='page-link' onclick='searchText(event);' page='" +
            j +
            "'  >" +
            j +
            "</a></li>"
        );
      }
    }

    $.ajax({
      method: "POST",
      url: '{{ url_for("store.descriptionsIndex")|tojson }}',
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        textoABuscar: texto,
        padministration: padministrationSel,
        domain: domainSel,
        page: page,
      }),
    }).done(addShow);
  }
}

function createNew(event) {
  if (event.type == "click") {
    window.location = "/descriptionDetail";
  }
}
