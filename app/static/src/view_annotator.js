/*
Annotator view panel Plugin v1.0 (https://https://github.com/albertjuhe/annotator_view/)
Copyright (C) 2014 Albert Juhé Brugué
License: https://github.com/albertjuhe/annotator_view/License.rst

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
*/

(function () {
  var __bind = function (fn, me) {
      return function () {
        return fn.apply(me, arguments);
      };
    },
    __hasProp = {}.hasOwnProperty,
    __extends = function (child, parent) {
      for (var key in parent) {
        if (__hasProp.call(parent, key)) child[key] = parent[key];
      }
      function ctor() {
        this.constructor = child;
      }
      ctor.prototype = parent.prototype;
      child.prototype = new ctor();
      child.__super__ = parent.prototype;
      return child;
    };

  var pathOrigen = document
    .getElementById("databackend")
    .getAttribute("basepath");

  //constants
  var IMAGE_DELETE = pathOrigen + "/static/src/img/icono_eliminar.png",
    IMAGE_DELETE_OVER = pathOrigen + "/static/src/img/papelera_over.png",
    SHARED_ICON = pathOrigen + "/static/src/img/shared-icon.png",
    IMAGE_REPLY = pathOrigen + "/static/src/img/reply.png",
    IMAGE_REPLY_OVER = pathOrigen + "/static/src/img/reply_over.png";
  Annotator.Plugin.AnnotatorViewer = (function (_super) {
    __extends(AnnotatorViewer, _super);

    AnnotatorViewer.prototype.events = {
      annotationsLoaded: "onAnnotationsLoaded",
      annotationCreated: "onAnnotationCreated",
      annotationDeleted: "onAnnotationDeleted",
      annotationReply: "onAnnotationReply",
      annotationUpdated: "onAnnotationUpdated",
      annotationCollapse: "onAnnotationCollapse",
      ".annotator-viewer-delete click": "onDeleteClick",
      ".annotator-viewer-edit click": "onEditClick",
      ".annotator-viewer-reply click": "onReplyClick",
      ".annotator-viewer-like click": "onLikeClick",
      ".annotator-viewer-collapse click": "onCollapseClick",
      ".annotator-viewer-delete mouseover": "onDeleteMouseover",
      ".annotator-viewer-delete mouseout": "onDeleteMouseout",
      ".annotator-viewer-reply mouseover": "onReplyMouseover",
      ".annotator-viewer-reply mouseout": "onReplyMouseout",
      ".annotator-viewer-like mouseover": "onLikeMouseover",
      ".annotator-viewer-like mouseout": "onLikeMouseout",
    };

    AnnotatorViewer.prototype.field = null;

    AnnotatorViewer.prototype.input = null;

    AnnotatorViewer.prototype.options = {
      AnnotatorViewer: {},
    };

    function AnnotatorViewer(element, options) {
      this.onAnnotationsLoaded = __bind(this.onAnnotationsLoaded, this);
      this.onAnnotationCreated = __bind(this.onAnnotationCreated, this);
      this.onAnnotationUpdated = __bind(this.onAnnotationUpdated, this);
      this.onDeleteClick = __bind(this.onDeleteClick, this);
      this.onEditClick = __bind(this.onEditClick, this);
      this.onDeleteMouseover = __bind(this.onDeleteMouseover, this);
      this.onDeleteMouseout = __bind(this.onDeleteMouseout, this);

      this.onReplyClick = __bind(this.onReplyClick, this);
      this.onReplyMouseover = __bind(this.onReplyMouseover, this);
      this.onReplyMouseout = __bind(this.onReplyMouseout, this);

      this.onLikeClick = __bind(this.onLikeClick, this);
      this.onLikeMouseover = __bind(this.onLikeMouseover, this);
      this.onLikeMouseout = __bind(this.onLikeMouseout, this);

      this.onCollapseClick = __bind(this.onCollapseClick, this);
      this.onCancelPanel = __bind(this.onCancelPanel, this);
      this.onSavePanel = __bind(this.onSavePanel, this);

      this.onCancelPanelReply = __bind(this.onCancelPanelReply, this);
      this.onSavePanelReply = __bind(this.onSavePanelReply, this);

      AnnotatorViewer.__super__.constructor.apply(this, arguments);

      $("body").append(this.createAnnotationPanel());

      $(".container-anotacions").toggle();
      $("#annotations-panel").click(function (event) {
        $(".container-anotacions").toggle("slide");
      });
    }

    AnnotatorViewer.prototype.pluginInit = function () {
      if (!Annotator.supported()) {
        return;
      }

      $("#type_share").click(this.onFilter);
      $("#type_own").click(this.onFilter);
    };

    /*
    Check the checkboxes filter to search the annotations to show.
    Shared annotations have the class shared
    My annotations have the me class
    */
    AnnotatorViewer.prototype.onFilter = function (event) {
      var annotations_panel = $(".container-anotacions").find(
        ".annotator-marginviewer-element"
      );
      $(annotations_panel).hide();

      var class_view = "";

      var checkbox_selected = $("li.filter-panel").find("input:checked");
      if (checkbox_selected.length > 0) {
        $("li.filter-panel")
          .find("input:checked")
          .each(function () {
            class_view += $(this).attr("rel") + ".";
          });
        $(
          ".container-anotacions > li." +
            class_view.substring(0, class_view.length - 1)
        ).show();
      } else {
        $(annotations_panel).show();
      }
    };

    AnnotatorViewer.prototype.onDeleteClick = function (event) {
      event.stopPropagation();
      if (confirm(i18n_dict.confirm_delete)) {
        this.click;
        return this.onButtonClick(event, "delete");
      }
      return false;
    };

    AnnotatorViewer.prototype.onReplyClick = function (event) {
      event.stopPropagation();
      this.click;
      return this.onButtonClick(event, "reply");
    };

    AnnotatorViewer.prototype.onLikeClick = function (event) {
      event.stopPropagation();
      this.click;

      var valorClassAttr = $(event.target).attr("class");
      if (valorClassAttr.includes("solid")) {
        $(event.target).attr(
          "class",
          "fa-regular fa-heart annotator-viewer-like  fa-lg"
        );
      } else {
        $(event.target).attr(
          "class",
          "fa-solid fa-heart annotator-viewer-like  fa-lg"
        );
      }

      return this.onButtonClick(event, "like");
    };

    AnnotatorViewer.prototype.onCollapseClick = function (event) {
      event.stopPropagation();
      this.click;

      return this.onButtonClick(event, "collapse");
    };

    AnnotatorViewer.prototype.onEditClick = function (event) {
      event.stopPropagation();
      return this.onButtonClick(event, "edit");
    };

    AnnotatorViewer.prototype.onButtonClick = function (event, type) {
      var item;
      //item contains all the annotation information, this information is stored in an attribute called data-annotation.
      item = $(event.target).parents(".annotator-marginviewer-element");
      var servicepediaPath = document
        .getElementById("databackend")
        .getAttribute("servicepediapath");

      var opcionCollapse = "expandir";

      //Iconos de expand and collapse
      const labelExpand =
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path><path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"></path></svg>';
      const labelCollapse =
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"></path></svg>';

      if (type == "collapse") {
        //Obtengo el codigo de la annotation root to collapse
        anotationTagId = item[0]["id"];

        justId = anotationTagId.substring(11);
        let codText = $("#nrep-" + justId).attr("class");
        let result = codText.includes("isexpand");

        if (result) {
          opcionCollapse = "colapsar";
          $("#nrep-" + justId)
            .empty()
            .append(labelCollapse);
          $("#nrep-" + justId).addClass("iscollapsed");
          $("#nrep-" + justId).removeClass("isexpand");
        } else {
          $("#nrep-" + justId)
            .empty()
            .append(labelExpand);
          $("#nrep-" + justId).addClass("isexpand");
          $("#nrep-" + justId).removeClass("iscollapsed");
        }

        //Obtengo todos los replies de este tag

        function getReplies(idAnnotation, listReplies) {
          //Obtengo los hijos
          var listHijos = [];
          var listAnnotationsTags = $("li.annotator-marginviewer-element");
          for (let i = 0; i < listAnnotationsTags.length; i++) {
            itemTag = listAnnotationsTags[i];

            let hijoTag = itemTag["children"][0];
            existeContainerReply = false;
            if ("flex-replyContainer" == hijoTag["className"]) {
              existeContainerReply = true;
            }

            if (existeContainerReply) {
              annotationId = itemTag.getAttribute("id");
              annotationRef = hijoTag.getAttribute("idannotationref");

              if (annotationRef == idAnnotation) {
                listHijos.push(annotationId);
              }
            }
          }

          if (listHijos.length > 0) {
            listReplies.push(listHijos);

            //Recorro cada hijo buscando relacionados:

            for (itemHijo in listHijos) {
              itemValue = listHijos[itemHijo];

              if (itemValue === undefined) {
              } else {
                idHijo = itemValue;

                listReplies = getReplies(idHijo, listReplies);
              }
            }
          }

          return listReplies.flat();
        }

        //Remuevo todos los hijos
        //Obtengo hijos
        var listReplies = [];
        listReplies = getReplies(anotationTagId, listReplies);

        for (const key in listReplies) {
          tagAnnot = document.getElementById(listReplies[key]);

          //componentTagConflict= $("li.annotator-marginviewer-element"+'#'+listReplies[key]);

          if (opcionCollapse == "expandir") {
            // if (tagAnnot.hidden == true) {

            iconoBtn = tagAnnot.getAttribute("class"); // [0]['attributes'][4]['value'].split(" ")[1];
            idRep = tagAnnot.getAttribute("id").substring(11);

            //Muestro solamente los hijos del primer nivel:

            if (tagAnnot.getAttribute("idlink") == anotationTagId) {
              tagAnnot.hidden = false;

              //With Jquery
              $(
                "li.annotator-marginviewer-element" + "#" + listReplies[key]
              ).addClass("found");
              $(
                "li.annotator-marginviewer-element" + "#" + listReplies[key]
              ).show();

              //Pongo todos los iconos como comprimidos

              //   $('#nrep-'+anotationTagId).html(labelExpand);

              $("#nrep-" + idRep)
                .empty()
                .append(labelCollapse);
              $("#nrep-" + idRep).addClass("iscollapsed");
              $("#nrep-" + idRep).removeClass("isexpand");
            }
          } else {
            tagAnnot.hidden = true;

            //With Jquery
            $(
              "li.annotator-marginviewer-element" + "#" + listReplies[key]
            ).removeClass("found");
            $(
              "li.annotator-marginviewer-element" + "#" + listReplies[key]
            ).hide();
          }
        }

        //Obtengo el listado de todos los tags de anotaciones
        // var listaAnnotations=$("li.annotator-marginviewer-element");
        // for (const key in listaAnnotations) {

        //   tagAnnot=document.getElementById(listaAnnotations[key].getAttribute('id'));

        //   if (tagAnnot.hasAttribute('idlink')){

        //     itemAnnotationId=listaAnnotations[key].getAttribute('idlink');
        //     if(itemAnnotationId==anotationTagId){

        //       tagAnnot=document.getElementById(listaAnnotations[key].getAttribute('id'));

        //       if(tagAnnot.hidden == true){
        //         tagAnnot.hidden = false;
        //       }else{
        //         tagAnnot.hidden = true;
        //       }

        //     }

        //   }
        // }

        /*
if(divreply.is(":hidden")){
        divreply.attr('hidden', false);
      }
*/

        return item.data("annotation");
      }

      if (type == "delete") {
        return this.annotator.deleteAnnotation(item.data("annotation"));
      }
      if (type == "reply") {
        //console.log("Ha entrado en la accion de reply");

        var annotator_textArea = item.find("div.annotator-marginviewer-reply");
        annotator_textArea = annotator_textArea.find("div.anotador_text");

        //Obtengo los valores:
        idReferencia = annotator_textArea.prevObject.prevObject[0].id;
        //item.id = idReferencia.split("-")[1];

        let listSubtrings = idReferencia.split("-");
        item.id = listSubtrings.slice(1, listSubtrings.leght).join("-");

        var localInstance = this;

        async function doAjax(item) {
          const result = await $.ajax({
            url: servicepediaPath + "/annotations/" + item.id,
            dataType: "json",
            type: "get",
            contentType: "application/json",
            processData: false,
          });

          return result;
        }

        doAjax(item).then((item) => {
          $("#annotation-" + item.id).data(item);
          this.textareaEditorReply(annotator_textArea, item);
        });
      }

      if (type == "like") {
        //

        //Punto de acceso:
        ///subjectPage/<string:descriptionId>/<string:annotatorId>/<string:option>

        //Registro el like de la anotacion:
        var servicepediaPath = document
          .getElementById("databackend")
          .getAttribute("servicepediapath");

        xmlhttp = new XMLHttpRequest();

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const descriptionId = urlParams.get("description");

        //annotatorId=item[0]["id"].split("-")[1];

        let listSubtrings = item[0]["id"].split("-");
        annotatorId = listSubtrings.slice(1, listSubtrings.leght).join("-");

        const urlpost =
          servicepediaPath +
          `/subjectPage/${descriptionId}/${annotatorId}/like`;

        xmlhttp.open("POST", urlpost, true);

        xmlhttp.setRequestHeader(
          "Content-type",
          "application/json;charset=UTF-8"
        );

        let timeSpentOnPage = TimeMe.getTimeOnAllPagesInSeconds();

        xmlhttp.send(
          JSON.stringify({
            stateToChange: "1",
            commentsChangeState: "",
            objtype: "annotation.like",
          })
        );
        //alert('You have successfully registered a like!');
      }

      /*let annotator_textArea=item.find("div.anotador_text");
        this.textareaEditor(annotator_textArea,item.data("annotation"))*/
      //this.annotator.replyAnnotation(item.data("annotation"));

      if (type == "edit") {
        //console.log("Ha entrado en la accion de edit");

        var annotator_textArea = item.find("div.annotator-marginviewer-text");
        annotator_textArea = annotator_textArea.find("div.anotador_text");

        //Obtengo los valores:
        idReferencia = annotator_textArea.prevObject.prevObject[0].id;
        //item.id = idReferencia.split("-")[1];

        let listSubtrings = idReferencia.split("-");
        item.id = listSubtrings.slice(1, listSubtrings.leght).join("-");

        var localInstance = this;

        async function doAjax(item) {
          const result = await $.ajax({
            url: servicepediaPath + "/annotations/" + item.id,
            dataType: "json",
            type: "get",
            contentType: "application/json",
            processData: false,
          });

          return result;
        }

        doAjax(item).then((item) => {
          $("#annotation-" + item.id).data(item);
          this.textareaEditor(annotator_textArea, item);
        });

        //We want to transform de div to a textarea
        //Find the text field
        //var annotator_divText = item.find("div.annotator-marginviewer-text")
        // var annotator_textArea = annotator_divText.find("div.anotador_text");
        // this.textareaEditor(annotator_textArea, item.data("annotation"));
      }
    };

    //Textarea editor controller
    AnnotatorViewer.prototype.textareaEditor = function (
      annotator_textArea,
      item
    ) {
      //Cambio el id del campo
      idReferencia = item.id;
      $("li#annotation-" + idReferencia).attr("id", "annotation-" + item.id);

      //First we have to get the text, if no, we will have an empty text area after replace the div
      if (
        $("li#annotation-" + item.id).find("textarea.panelTextArea").length == 0
      ) {
        var content = item.text;
        var editableTextArea = $(
          "<textarea id='textarea-" +
            item.id +
            "'' class='panelTextArea'>" +
            content +
            "</textarea>"
        );
        var annotationCSSReference =
          "li#annotation-" + item.id + " > div.annotator-marginviewer-text";

        annotator_textArea.replaceWith(editableTextArea);
        editableTextArea.css("height", editableTextArea[0].scrollHeight + "px");
        editableTextArea.blur(); //Textarea blur
        if (typeof this.annotator.plugins.RichEditor != "undefined") {
          this.tinymceActivation(
            annotationCSSReference + " > textarea#textarea-" + item.id
          );
        }
        $(
          '<div class="annotator-textarea-controls annotator-editor"></div>'
        ).insertAfter(editableTextArea);
        var control_buttons = $(
          annotationCSSReference + "> .annotator-textarea-controls"
        );

        saveTxt = i18n_dict.Save;
        cancelTxt = i18n_dict.Cancel;

        $(`<a href="#save" class="annotator-panel-save">${saveTxt}</a>`)
          .appendTo(control_buttons)
          .bind("click", { annotation: item }, this.onSavePanel);
        $(`<a href="#cancel" class="annotator-panel-cancel">${cancelTxt}</a>`)
          .appendTo(control_buttons)
          .bind("click", { annotation: item }, this.onCancelPanel);
      }
    };

    //Textarea editor controller
    AnnotatorViewer.prototype.textareaEditorReply = function (
      annotator_textArea,
      item
    ) {
      idReferencia = annotator_textArea.prevObject.prevObject[0].id;
      //item.id = idReferencia.split("-")[1];
      let listSubtrings = idReferencia.split("-");
      item.id = listSubtrings.slice(1, listSubtrings.leght).join("-");

      //Busco si ya fue cargado

      var divreply = $("li#annotation-" + item.id).find(
        "div.annotator-marginviewer-reply"
      );

      if (divreply.is(":hidden")) {
        divreply.attr("hidden", false);
      } else {
        //Cambio el id del campo
        //idReferencia=item.highlights[0].id
        $("li#annotation-" + idReferencia).attr("id", "annotation-" + item.id);

        //First we have to get the text, if no, we will have an empty text area after replace the div
        if (
          $("li#annotation-" + item.id).find("textarea.panelTextAreaReply")
            .length == 0
        ) {
          var editableTextAreaReply = $(
            "<textarea id='textareaReply-" +
              item.id +
              "'' class='panelTextAreaReply'>" +
              "" +
              "</textarea>"
          );

          if (item.category == "reply") {
            var annotationCSSReference =
              "li#annotation-" +
              item.id +
              "> div.flex-replyContainer > div.annotator-marginviewer-reply";
          } else {
            var annotationCSSReference =
              "li#annotation-" +
              item.id +
              " > div.annotator-marginviewer-reply";
          }

          annotator_textArea.replaceWith(editableTextAreaReply);
          editableTextAreaReply.css(
            "height",
            editableTextAreaReply[0].scrollHeight + "px"
          );
          editableTextAreaReply.blur(); //Textarea blur
          if (typeof this.annotator.plugins.RichEditor != "undefined") {
            this.tinymceActivation(
              annotationCSSReference + " > textarea#textareaReply-" + item.id
            );
          }
          $(
            '<div class="annotator-textarea-controls annotator-editor"></div>'
          ).insertAfter(editableTextAreaReply);
          var control_buttons = $(
            annotationCSSReference + "> .annotator-textarea-controls"
          );

          saveTxt = i18n_dict.Save;
          cancelTxt = i18n_dict.Cancel;

          $(`<a href="#save" class="annotator-panel-save">${saveTxt}</a>`)
            .appendTo(control_buttons)
            .bind("click", { annotation: item }, this.onSavePanelReply);
          $(`<a href="#cancel" class="annotator-panel-cancel">${cancelTxt}</a>`)
            .appendTo(control_buttons)
            .bind("click", { annotation: item }, this.onCancelPanelReply);
        }
      }
    };

    AnnotatorViewer.prototype.tinymceActivation = function (selector) {
      tinymce.init({
        selector: selector,
        height: 200,
        resize: false,

        plugins: "media image insertdatetime link",
        menubar: false,
        statusbar: false,
        toolbar_items_size: "small",
        extended_valid_elements: "",
        paste_as_text: true,
        toolbar:
          "undo redo link image media bold italic alignleft aligncenter alignright alignjustify",
      });
    };

    //Event triggered when save the content of the annotation
    AnnotatorViewer.prototype.onSavePanel = function (event) {
      var current_annotation = event.data.annotation;
      var textarea = $("li#annotation-" + current_annotation.id).find(
        "#textarea-" + current_annotation.id
      );
      if (typeof this.annotator.plugins.RichEditor != "undefined") {
        current_annotation.text = tinymce.activeEditor.getContent();
        //tinymce.remove("#textarea-" + current_annotation.id);
        tinymce.EditorManager.remove(".editable");

        tinymce.activeEditor.setContent(current_annotation.text);
      } else {
        current_annotation.text = textarea.val();
        //this.normalEditor(current_annotation,textarea);
      }
      var anotation_reference = "annotation-" + current_annotation.id;
      $("#" + anotation_reference).data("annotation", current_annotation);
      //console.log(this.annotations);
      this.annotator.updateAnnotation(current_annotation);

      //Actualizo los datos que tienen los highliths.
      $("span#" + current_annotation.id).data("annotation", current_annotation);
    };

    //Event triggered when save the content of the annotation
    AnnotatorViewer.prototype.onSavePanelReply = function (event) {
      var current_annotation = event.data.annotation;
      var textarea = $("li#annotation-" + current_annotation.id).find(
        "#textareaReply-" + current_annotation.id
      );
      if (typeof this.annotator.plugins.RichEditor != "undefined") {
        textReply = tinymce.activeEditor.getContent();
        //tinymce.remove("#textareaReply-" + current_annotation.id);
        tinymce.EditorManager.remove(".editable");
        tinymce.activeEditor.setContent(textReply);
      } else {
        textReply = textareaReply.val();
        //this.normalEditor(current_annotation,textareaReply);
      }
      var anotation_reference = "annotation-" + current_annotation.id;
      $("#" + anotation_reference).data("annotation", current_annotation);

      //Arreglo el URL
      current_annotation.uri;

      //Hago una copia de la anotación de referencia:
      let anotacionReply = JSON.parse(JSON.stringify(current_annotation));

      let str = current_annotation.uri;
      const myArr = str.split("http");
      anotacionReply.uri = "http" + myArr[myArr.length - 1];

      anotacionReply.id = this.uniqId();
      anotacionReply.text = textReply;
      anotacionReply.idAnotationReply = anotation_reference;
      anotacionReply.user = "MeAnotator";

      var currentuser = document
        .getElementById("databackend")
        .getAttribute("currentuser");
      anotacionReply.user = currentuser;

      anotacionReply.permissions.delete = [currentuser];

      anotacionReply.category = "reply";

      /* Guardo tambien el valor del annotation-root si existe,
         caso contrario ingreso le asigno el mismo que el reference 
      */

      if (
        current_annotation.idReplyRoot == "" ||
        typeof current_annotation.idReplyRoot == "undefined"
      ) {
        anotacionReply.idReplyRoot = current_annotation.id;
      } else {
        anotacionReply.idReplyRoot = current_annotation.idReplyRoot;
      }

      /*

      function onSuccess(response) {
        //alert("Se ha insertado exitosamente");
      }

      request = $.ajax({
        url: "http://127.0.0.1:80/annotations",
        dataType: "json",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(anotacionReply),
        processData: false,
        success: onSuccess || function () {},
        error: function (jqXhr, textStatus, errorThrown) {
          console.log(errorThrown);
        },
      });

      var current_annotation = event.data.annotation;
      var styleHeight = 'style="height:12px"';

      


      this.createReferenceAnnotation(anotacionReply);
      $("#count-anotations").text(
        $(".container-anotacions").find(".annotator-marginviewer-element")
          .length
      );

      */

      function removeAllChildNodes(parent) {
        while (parent.firstChild) {
          parent.removeChild(parent.firstChild);
        }

        let divAText = document.createElement("div");
        divAText.classList.add("anotador_text");
        parent.appendChild(divAText);
      }

      removeAllChildNodes(event.currentTarget.parentNode.parentNode);

      this.publish("annotationCreated", [anotacionReply]);
      //this.publish("beforeAnnotationCreated", [anotacionReply]);
      //this.annotation.createAnnotation()
      //this.annotator.updateAnnotation(current_annotation);
    };

    //Event triggered when save the content of the annotation
    AnnotatorViewer.prototype.onCancelPanel = function (event) {
      var current_annotation = event.data.annotation;
      var styleHeight = 'style="height:12px"';
      if (current_annotation.text.length > 0) styleHeight = "";

      if (typeof this.annotator.plugins.RichEditor != "undefined") {
        //tinymce.remove("#textarea-" + current_annotation.id);

        //Compruebo si el textarea ya fue cargado
        //Si es asi solamente le pongo visible=true.
        //Caso contrario le pongo hidden al tag.

        // var divreply = $("li#annotation-" + current_annotation.id).find(
        //   "div.tox-tinymce"
        // );

        // divreply.attr('hidden', true);

        tinymce.EditorManager.remove(".editable");
        var textAnnotation =
          '<div class="anotador_text" ' +
          styleHeight +
          ">" +
          current_annotation.text +
          "</div>";

        var anotacio_capa =
          '<div class="annotator-marginviewer-text">' +
          '<div class="' +
          current_annotation.category +
          ' anotator_color_box"></div>' +
          textAnnotation +
          "</div>";

        var textAreaEditor = $(
          "li#annotation-" +
            current_annotation.id +
            " > .annotator-marginviewer-text"
        );
        textAreaEditor.replaceWith(anotacio_capa);
      } else {
        var textarea = $("li#annotation-" + current_annotation.id).find(
          "textarea.panelTextArea"
        );
        this.normalEditor(current_annotation, textarea);
      }
    };

    //Event triggered when save the content of the annotation
    AnnotatorViewer.prototype.onCancelPanelReply = function (event) {
      var current_annotation = event.data.annotation;
      var styleHeight = 'style="height:12px"';
      if (current_annotation.text.length > 0) styleHeight = "";

      if (typeof this.annotator.plugins.RichEditor != "undefined") {
        //tinymce.remove("#textareaReply-" + current_annotation.id);

        //Compruebo si el textarea ya fue cargado
        //Si es asi solamente le pongo visible=true.
        //Caso contrario le pongo hidden al tag.

        var divreply = $("li#annotation-" + current_annotation.id).find(
          "div.annotator-marginviewer-reply"
        );

        divreply.attr("hidden", true);

        // tinymce.EditorManager.remove(".editable");

        // var textAnnotation =
        //   '<div class="anotador_text" ' + styleHeight + ">" + "" + "</div>";

        // var anotacio_capa =
        //   '<div class="annotator-marginviewer-reply">' +
        //   textAnnotation +
        //   "</div>";

        // if (current_annotation.category == "reply") {
        //   var textAreaEditorReply = $(
        //     "li#annotation-" +
        //       current_annotation.id +
        //       " > .flex-replyContainer > .annotator-marginviewer-reply"
        //   );
        // } else {
        //   var textAreaEditorReply = $(
        //     "li#annotation-" +
        //       current_annotation.id +
        //       " > .annotator-marginviewer-reply"
        //   );
        // }

        // textAreaEditorReply.replaceWith(anotacio_capa);
      } else {
        var textarea = $("li#annotation-" + current_annotation.id).find(
          "textarea.panelTextAreaReply"
        );
        this.normalEditor(current_annotation, textarea);
      }
    };

    //Annotator in a non editable state
    AnnotatorViewer.prototype.normalEditor = function (
      annotation,
      editableTextArea
    ) {
      var buttons = $("li#annotation-" + annotation.id).find(
        "div.annotator-textarea-controls"
      );
      var textAnnotation = this.removeTags("iframe", annotation.text);
      editableTextArea.replaceWith(
        '<div class="anotador_text">' + textAnnotation + "</div>"
      );
      buttons.remove();
    };

    AnnotatorViewer.prototype.onDeleteMouseover = function (event) {
      $(event.target).attr("src", IMAGE_DELETE_OVER);
    };

    AnnotatorViewer.prototype.onLikeMouseover = function (event) {
      var valorClassAttr = $(event.target).attr("class");
      if (valorClassAttr.includes("solid")) {
        $(event.target).attr(
          "class",
          "fa-regular fa-heart annotator-viewer-like  fa-lg"
        );
      } else {
        $(event.target).attr(
          "class",
          "fa-solid fa-heart annotator-viewer-like  fa-lg"
        );
      }
    };

    AnnotatorViewer.prototype.onLikeMouseout = function (event) {
      var valorClassAttr = $(event.target).attr("class");
      if (valorClassAttr.includes("solid")) {
        $(event.target).attr(
          "class",
          "fa-regular fa-heart annotator-viewer-like  fa-lg"
        );
      } else {
        $(event.target).attr(
          "class",
          "fa-solid fa-heart annotator-viewer-like  fa-lg"
        );
      }
    };

    AnnotatorViewer.prototype.onReplyMouseover = function (event) {
      $(event.target).attr("src", IMAGE_REPLY_OVER);
    };

    AnnotatorViewer.prototype.onDeleteMouseout = function (event) {
      $(event.target).attr("src", IMAGE_DELETE);
    };

    AnnotatorViewer.prototype.onReplyMouseout = function (event) {
      $(event.target).attr("src", IMAGE_REPLY);
    };

    AnnotatorViewer.prototype.onAnnotationCreated = function (annotation) {
      this.createReferenceAnnotation(annotation);
      $("#count-anotations").text(
        $(".container-anotacions").find(".annotator-marginviewer-element")
          .length
      );
    };
    function htmlEntities(str) {
      return String(str)
        .replace("&ntilde;", "ñ")
        .replace("&Ntilde;", "Ñ")
        .replace("&amp;", "&")
        .replace("&Ntilde;", "Ñ")
        .replace("&ntilde;", "ñ")
        .replace("&Ntilde;", "Ñ")
        .replace("&Agrave;", "À")
        .replace("&Aacute;", "Á")
        .replace("&Acirc;", "Â")
        .replace("&Atilde;", "Ã")
        .replace("&Auml;", "Ä")
        .replace("&Aring;", "Å")
        .replace("&AElig;", "Æ")
        .replace("&Ccedil;", "Ç")
        .replace("&Egrave;", "È")
        .replace("&Eacute;", "É")
        .replace("&Ecirc;", "Ê")
        .replace("&Euml;", "Ë")
        .replace("&Igrave;", "Ì")
        .replace("&Iacute;", "Í")
        .replace("&Icirc;", "Î")
        .replace("&Iuml;", "Ï")
        .replace("&ETH;", "Ð")
        .replace("&Ntilde;", "Ñ")
        .replace("&Ograve;", "Ò")
        .replace("&Oacute;", "Ó")
        .replace("&Ocirc;", "Ô")
        .replace("&Otilde;", "Õ")
        .replace("&Ouml;", "Ö")
        .replace("&Oslash;", "Ø")
        .replace("&Ugrave;", "Ù")
        .replace("&Uacute;", "Ú")
        .replace("&Ucirc;", "Û")
        .replace("&Uuml;", "Ü")
        .replace("&Yacute;", "Ý")
        .replace("&THORN;", "Þ")
        .replace("&szlig;", "ß")
        .replace("&agrave;", "à")
        .replace("&aacute;", "á")
        .replace("&acirc;", "â")
        .replace("&atilde;", "ã")
        .replace("&auml;", "ä")
        .replace("&aring;", "å")
        .replace("&aelig;", "æ")
        .replace("&ccedil;", "ç")
        .replace("&egrave;", "è")
        .replace("&eacute;", "é")
        .replace("&ecirc;", "ê")
        .replace("&euml;", "ë")
        .replace("&igrave;", "ì")
        .replace("&iacute;", "í")
        .replace("&icirc;", "î")
        .replace("&iuml;", "ï")
        .replace("&eth;", "ð")
        .replace("&ntilde;", "ñ")
        .replace("&ograve;", "ò")
        .replace("&oacute;", "ó")
        .replace("&ocirc;", "ô")
        .replace("&otilde;", "õ")
        .replace("&ouml;", "ö")
        .replace("&oslash;", "ø")
        .replace("&ugrave;", "ù")
        .replace("&uacute;", "ú")
        .replace("&ucirc;", "û")
        .replace("&uuml;", "ü")
        .replace("&yacute;", "ý")
        .replace("&thorn;", "þ")
        .replace("&yuml;", "ÿ");
    }

    AnnotatorViewer.prototype.onAnnotationUpdated = function (annotation) {
      idAnotacionReferencia = annotation.id;

      $("#annotation-" + idAnotacionReferencia).html(
        this.mascaraAnnotation(annotation)
      );

      $("#annotation-" + annotation.id).html(
        this.mascaraAnnotation(annotation)
      );

      idAnotacion = annotation.id;

      let strippedHtmlText = annotation.text.replace(/<[^>]+>/g, "");
      strippedHtmlText = htmlEntities(strippedHtmlText);

      var servicepediaPath = document
        .getElementById("databackend")
        .getAttribute("servicepediapath");

      $(
        "#annotation-" +
          idAnotacion +
          " .annotator-marginviewer-text .anotador_text"
      ).text(strippedHtmlText);

      request = $.ajax({
        url: servicepediaPath + "/annotations/" + annotation.id,
        dataType: "json",
        type: "put",
        contentType: "application/json",
        data: JSON.stringify(annotation),
        processData: false,
        success: function () {},
        error: function (jqXhr, textStatus, errorThrown) {
          console.log(errorThrown);
        },
      });
    };

    AnnotatorViewer.prototype.onAnnotationsLoaded = function (annotations) {
      var annotation;

      function showOrder(
        annotationIn = null,
        anotationList = [],
        categoria = "",
        referenciaThis,
        level = 0
      ) {
        if (annotationIn == null) {
          var listAnnotationsNoReply = anotationList.filter(
            (annotation) => annotation.category != "reply"
          );
          listAnnotationsNoReply.forEach((element) =>
            showOrder(
              element,
              anotationList,
              (categoria = "reply"),
              referenciaThis,
              (level = 0)
            )
          );
        } else {
          annotationIn["level"] = level;
          referenciaThis.createReferenceAnnotation(annotationIn);
          level = level + 1;
          var listAnnotations = anotationList.filter(
            (annotation) =>
              annotation.idAnotationReply == "annotation-" + annotationIn.id
          );
          listAnnotations.forEach((element) =>
            showOrder(
              element,
              anotationList,
              (categoria = "reply"),
              referenciaThis,
              (level = level)
            )
          );
        }
      }

      function arrayRemove(arr, value) {
        return arr.filter(function (ele) {
          return ele != value;
        });
      }

      showOrder(null, annotations, "", (referenciaThis = this));

      /*
      if (annotations.length > 0) {
        for (i = 0, len = annotations.length; i < len; i++) {
          annotation = annotations[i];
          //console.log(annotation.uri)
          if(annotation.category!="reply"){
            this.createReferenceAnnotation(annotation);

            //Busco Reply of the Annotation
            var annotationReply;
            for (j = 0, len = annotations.length; j < len; j++) {
              annotationReply = annotations[j];
              if(annotationReply.category=="reply" && annotationReply.idAnotationReply=="annotation-"+annotation.id){

                //console.log(annotation.uri)
                this.createReferenceAnnotation(annotationReply);
              }
              
            }
      
          }


        }
      }*/

      /* if (annotations.length > 0) {
        for (i = 0, len = annotations.length; i < len; i++) {
          annotation = annotations[i];
          //console.log(annotation.uri)
          this.createReferenceAnnotation(annotation);
        }
      }*/

      $("#count-anotations").text(
        $(".container-anotacions").find(".annotator-marginviewer-element")
          .length
      );

      //Agrego los numeros de rep a los nodos:

      //Obtengo todas las anotaciones
      const listAnnotationsTags = $(".container-anotacions").find(
        ".annotator-marginviewer-element"
      );

      var listIds = [];
      for (let i = 0; i < listAnnotationsTags.length; i++) {
        itemTag = listAnnotationsTags[i];
        annotationId = itemTag.getAttribute("id");
        listIds.push(annotationId);
      }

      function getReplies1(idAnnotation, listReplies) {
        //Obtengo los hijos
        var listHijos = [];
        for (let i = 0; i < listAnnotationsTags.length; i++) {
          itemTag = listAnnotationsTags[i];

          let hijoTag = itemTag["children"][0];
          existeContainerReply = false;
          if ("flex-replyContainer" == hijoTag["className"]) {
            existeContainerReply = true;
          }

          if (existeContainerReply) {
            annotationId = itemTag.getAttribute("id");
            annotationRef = hijoTag.getAttribute("idannotationref");

            if (annotationRef == idAnnotation) {
              listHijos.push(annotationId);
            }
          }
        }

        if (listHijos.length > 0) {
          listReplies.push(listHijos);

          //Recorro cada hijo buscando relacionados:

          for (itemHijo in listHijos) {
            itemValue = listHijos[itemHijo];

            if (itemValue === undefined) {
            } else {
              idHijo = itemValue.substring(11, itemValue.length);

              listReplies = getReplies1(idHijo, listReplies);
            }
          }
        }

        return listReplies.flat();
      }

      listIds.forEach(function (item, index) {
        var listReplies = [];

        listHijos = getReplies1(item, listReplies);
        var idAnnotation = item.substring(11);
        if (listHijos.length > 0) {
          $("#nrep-" + idAnnotation).prepend("(" + listHijos.length + ")");
        } else {
          $("#nrep-" + idAnnotation).hide();
        }
      });

      // Abro el panel y cargo una annotacion especifica:
      const queryString = window.location.search;
      console.log(queryString);
      const urlParams = new URLSearchParams(queryString);
      const idAnnotation = urlParams.get("annotationId");
      const idDescription = urlParams.get("description");
      //alert('Identificador Annotation:'+annotationId);

      if (idAnnotation != null) {
        // Abro Panel:
        $(".container-anotacions").show();

        //Muestro la annotacion y sus replies:

        function getReplies(idAnnotation, listReplies) {
          //Obtengo los hijos
          var listHijos = [];
          var listAnnotationsTags = $("li.annotator-marginviewer-element");
          for (let i = 0; i < listAnnotationsTags.length; i++) {
            itemTag = listAnnotationsTags[i];

            let hijoTag = itemTag["children"][0];
            existeContainerReply = false;
            if ("flex-replyContainer" == hijoTag["className"]) {
              existeContainerReply = true;
            }

            if (existeContainerReply) {
              annotationId = itemTag.getAttribute("id");
              annotationRef = hijoTag.getAttribute("idannotationref");

              if (annotationRef == "annotation-" + idAnnotation) {
                listHijos.push(annotationId);
              }
            }
          }

          if (listHijos.length > 0) {
            listReplies.push(listHijos);

            //Recorro cada hijo buscando relacionados:

            for (itemHijo in listHijos) {
              itemValue = listHijos[itemHijo];

              if (itemValue === undefined) {
              } else {
                idHijo = itemValue;

                listReplies = getReplies(idHijo, listReplies);
              }
            }
          }

          return listReplies.flat();
        }

        $("li.annotator-marginviewer-element").each(function (index) {
          const annotationId = this["id"];

          //Obtengo los replies:
          let listReplies = [];
          listReplies = getReplies(idAnnotation, listReplies);

          if (annotationId.substring(11) == idAnnotation) {
            $(this).show();
          } else {
            if (listReplies.includes(annotationId)) {
              //With Jquery
              $(
                "li.annotator-marginviewer-element" + "#" + annotationId
              ).addClass("found");
              $(
                "li.annotator-marginviewer-element" + "#" + annotationId
              ).show();

              //Pongo todos los iconos como comprimidos
              const idRep = annotationId.substring(11);
              const labelCollapse =
                '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"></path></svg>';

              $("#nrep-" + idRep)
                .empty()
                .append(labelCollapse);
              $("#nrep-" + idRep).addClass("iscollapsed");
              $("#nrep-" + idRep).removeClass("isexpand");
            } else {
              $(this).hide();
            }
          }
        });

        //POngo el visor sobre la annotacion:

        var viewPanelHeight = jQuery(window).height();
        var annotation_reference = idAnnotation;

        $element = jQuery("#" + idAnnotation);
        // if (!$element.length) {
        //   $element = jQuery("#" + annotation.order);
        //   annotation_reference = annotation.order; //If exists a sorted annotations we put it in the right order, using order attribute
        // }

        if ($element.length) {
          elOffset = $element.offset();
          $(this).children(".annotator-marginviewer-quote").toggle();
          $("html, body").animate(
            {
              scrollTop:
                $("#" + annotation_reference).offset().top -
                viewPanelHeight / 2,
            },
            2000
          );
        }
      }

      //Obtengo todas las anotaciones
      const listAnnotationsTagsLast = $(".container-anotacions").find(
        ".annotator-marginviewer-element"
      );

      var listIds = [];
      for (let i = 0; i < listAnnotationsTagsLast.length; i++) {
        itemTag = listAnnotationsTagsLast[i];
        annotationId = itemTag.getAttribute("id");
        listIds.push(annotationId.substring(11));
      }

      function updateAnnotationsVisibles(accion, annotationId) {
        //Agregar una annotacion
        if (accion == "add") {
          //alert('agrego'+annotationId);

          //Obtengo la informacion de la annotacion:

          var servicepediaPath = document
            .getElementById("databackend")
            .getAttribute("servicepediapath");

          request = $.ajax({
            url: servicepediaPath + "/annotations/" + annotationId,
            dataType: "json",
            success: onSuccessAddGetAnot,
            error: function (jqXhr, textStatus, errorThrown) {
              console.log(errorThrown);
            },
          });

          function onSuccessAddGetAnot(data, status, xhr) {
            // success callback function
            anotacion = data;
            //Agrego la anotacion:

            var currentuser = document
              .getElementById("databackend")
              .getAttribute("currentuser");

            if (anotacion["user"] != currentuser) {
              //alert(anotacion['user']+ " ha agregado una annotacion");

              //notPublish por que la salida del metodo detiene las siguiente ejecución
              anotacion["notpublish"] = true;
              Annotator.prototype.loadAnnotations((annotations = [anotacion]));

              //Pongo la categoria correcta:
              classF = "annotator-hl-destacat";
              classQ = "annotator-hl-subratllat";
              classT = "annotator-hl-term";

              newClassCategory = "";
              if (anotacion["category"] == "feedback") {
                newClassCategory = classF;
              }
              if (anotacion["category"] == "question") {
                newClassCategory = classQ;
              }
              if (anotacion["category"] == "term") {
                newClassCategory = classT;
              }

              //Le agrego un identificador unico:
              $(".annotator-hl")
                .not("." + classF + ",." + classQ + ",." + classT)
                .attr("id", anotacion["id"]);
              //Le doy el formato de color:
              $(".annotator-hl")
                .not("." + classF + ",." + classQ + ",." + classT)
                .addClass(newClassCategory);

              AnnotatorViewer.prototype.createReferenceAnnotation(anotacion);

              // Annotator.prototype.onHighlightMouseoverEfect(anotacion);
            }
          }
        }

        if (accion == "remove") {
          //alert('quito'+annotationId);

          anotacion = $("#" + annotationId).data("annotation");

          if (anotacion != null) {
            //Quito los highlights:
            //Para que el metodo on delete no trate de borrarlo (solo quito highlights)
            anotacion["notpublish"] = true;
            Annotator.prototype.deleteAnnotation(anotacion);

            //Quito del Panel:
            AnnotatorViewer.prototype.onAnnotationDeleted(anotacion);

            //quitarHighlight(anotacion);
            //quitarSidePanel(anotacion);

            //Pongo el contador con el numero correcto:
            $("#count-anotations").text(
              $(".container-anotacions").find(".annotator-marginviewer-element")
                .length
            );
          }
        }
      }

      TimeMe.initialize({
        currentPageName: window.location.href, // current page
        idleTimeoutInSeconds: 5, // stop recording time due to inactivity
        //websocketOptions: { // optional
        //	websocketHost: "ws://your_host:your_port",
        //	appId: "insert-your-made-up-app-id"
        //}
      });

      /* TimeMe.callAfterTimeElapsedInSeconds(4, function () {
        console.log(
          "The user has been using the page for 4 seconds! Let's prompt them with something."
        );
      });

      TimeMe.callAfterTimeElapsedInSeconds(9, function () {
        console.log(
          "The user has been using the page for 9 seconds! Let's prompt them with something."
        );
      }); */

      window.onload = function () {
        //Obtengo todas las anotaciones
        const listAnnotationsTagsLast = $(".container-anotacions").find(
          ".annotator-marginviewer-element"
        );

        var listIds = [];
        for (let i = 0; i < listAnnotationsTagsLast.length; i++) {
          itemTag = listAnnotationsTagsLast[i];
          annotationId = itemTag.getAttribute("id");
          TimeMe.trackTimeOnElement(annotationId);
        }

        //TimeMe.trackTimeOnElement("area-of-interest-1");
        //TimeMe.trackTimeOnElement("area-of-interest-2");
        setInterval(function () {
          let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
          document.getElementById("timeInSeconds").textContent =
            timeSpentOnPage.toFixed(2);

          if (
            TimeMe.isUserCurrentlyOnPage &&
            TimeMe.isUserCurrentlyIdle === false
          ) {
            document.getElementById("activityStatus").textContent =
              "You are actively using this page.";
          } else {
            document.getElementById("activityStatus").textContent =
              "You have left the page.";
          }

          for (let i = 0; i < listAnnotationsTagsLast.length; i++) {
            itemTag = listAnnotationsTagsLast[i];
            annotationId = itemTag.getAttribute("id");
            let timeSpentOnElement =
              TimeMe.getTimeOnElementInSeconds(annotationId);
            if (document.getElementById("time-" + annotationId) == null) {
              //console.log("Este id no existe:"+"time-" + annotationId);
            } else {
              document.getElementById("time-" + annotationId).textContent =
                timeSpentOnElement.toFixed(2);
            }
          }

          /*let timeSpentOnElement =
           TimeMe.getTimeOnElementInSeconds("area-of-interest-1");
         document.getElementById("area-of-interest-time-1").textContent =
           timeSpentOnElement.toFixed(2);

         let timeSpentOnElement2 =
           TimeMe.getTimeOnElementInSeconds("area-of-interest-2");
         document.getElementById("area-of-interest-time-2").textContent =
           timeSpentOnElement2.toFixed(2);*/
        }, 37);
      };

      window.onbeforeunload = function (event) {
        var servicepediaPath = document
          .getElementById("databackend")
          .getAttribute("servicepediapath");

        xmlhttp = new XMLHttpRequest();

        const urlpost = servicepediaPath + "/logwithapi";

        xmlhttp.open("POST", urlpost, true);

        xmlhttp.setRequestHeader(
          "Content-type",
          "application/json;charset=UTF-8"
        );

        let timeSpentOnPage = TimeMe.getTimeOnAllPagesInSeconds();

        xmlhttp.send(JSON.stringify(timeSpentOnPage));
      };

      //Me conecto al socket
      var servicepediaPath = document
        .getElementById("databackend")
        .getAttribute("servicepediapath");
      const { hostname } = new URL(servicepediaPath);

      let puertoSocket = "80";
      let protocolSocket = "ws";
      if (hostname != "localhost") {
        puertoSocket = "443";
        protocolSocket = "wss";
      }

      // servicepedia.dev.interlink-project.eu
      let socket = new WebSocket(
        protocolSocket + "://" + hostname + ":" + puertoSocket + "/eventsocket"
      );

      socket.onopen = function (e) {
        //alert("[open] Connection established");
        //alert("Sending to server");
        //socket.send("My name is John");

        function buscoCambios() {
          //Obtengo todas las anotaciones
          const listAnnotationsTagsLast = $(".container-anotacions").find(
            ".annotator-marginviewer-element"
          );

          var listIds = [];
          for (let i = 0; i < listAnnotationsTagsLast.length; i++) {
            itemTag = listAnnotationsTagsLast[i];
            annotationId = itemTag.getAttribute("id");
            listIds.push(annotationId.substring(11));
          }

          const queryString = window.location.search;
          const urlParams = new URLSearchParams(queryString);
          const descriptionId = urlParams.get("description");

          socket.send(descriptionId + "#" + listIds.join());
          //alert('Se envian la description '+descriptionId);
        }

        //Comienzo un loop que pregunte cada 3 segundos

        function myLoop() {
          //  create a loop function
          setTimeout(function () {
            //  call a 3s setTimeout when the loop is called
            buscoCambios(); //  your code here
            //  increment the counter
            if (true) {
              //  if the counter < 10, call the loop function
              myLoop(); //  ..  again which will trigger another
            } //  ..  setTimeout()
          }, 5000);
        }

        myLoop();
      };

      socket.onmessage = function (event) {
        //alert(`[message] Data received from server: ${event.data}`);
        stringData = event.data.split("#");
        dataAccion = stringData[0];
        datalst = stringData[1];
        listIds = datalst.split(",");

        for (let i = 0; i < listIds.length; i++) {
          annotationId = listIds[i];
          updateAnnotationsVisibles(dataAccion, annotationId);
        }

        //Pongo el contador con el numero correcto:
        $("#count-anotations").text(
          $(".container-anotacions").find(".annotator-marginviewer-element")
            .length
        );
      };

      socket.onclose = function (event) {
        if (event.wasClean) {
          //alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
          // e.g. server process killed or network down
          // event.code is usually 1006 in this case
          //alert('[close] Connection died');
        }
      };

      socket.onerror = function (error) {
        alert(`[error] ${error.message}`);
      };
    };

    AnnotatorViewer.prototype.onAnnotationDeleted = function (annotation) {
      idAnotacionReferencia = annotation.id;

      //Miro si es posible eliminar la anotacion buscando por el texto
      $(".annotator-marginviewer-element").each(function (index, valor) {
        let anotacionId = valor.id;

        if ("annotation-" + idAnotacionReferencia == valor.id) {
          $("li").remove("#" + anotacionId);
        }

        let textoAnotacion = valor.children[0].text;
      });

      if (annotation.id != null) {
        //Antes de quitar esta annotation tengo que quitar todas las anotaciones hijas
        listAnnotationsTags = $(".container-anotacions").find(
          ".annotator-marginviewer-element"
        );

        function getReplies(idAnnotation, listReplies) {
          //Obtengo los hijos
          var listHijos = [];
          for (let i = 0; i < listAnnotationsTags.length; i++) {
            itemTag = listAnnotationsTags[i];

            let hijoTag = itemTag["children"][0];
            existeContainerReply = false;
            if ("flex-replyContainer" == hijoTag["className"]) {
              existeContainerReply = true;
            }

            if (existeContainerReply) {
              annotationId = itemTag.getAttribute("id");
              annotationRef = hijoTag.getAttribute("idannotationref");

              if (annotationRef == "annotation-" + idAnnotation) {
                listHijos.push(annotationId);
              }
            }
          }

          if (listHijos.length > 0) {
            listReplies.push(listHijos);

            //Recorro cada hijo buscando relacionados:

            for (itemHijo in listHijos) {
              itemValue = listHijos[itemHijo];

              if (itemValue === undefined) {
              } else {
                idHijo = itemValue.substring(11, itemValue.length);

                listReplies = getReplies(idHijo, listReplies);
              }
            }
          }

          return listReplies.flat();
        }

        //Remuevo todos los hijos
        //Obtengo hijos
        var listReplies = [];
        listReplies = getReplies(annotation.id, listReplies);

        //Quito todos los hijos relacionados de la lista
        for (itemReply in listReplies) {
          itemValor = listReplies[itemReply];
          $("li").remove("#" + itemValor);
        }

        $("li").remove("#annotation-" + annotation.id);
      }
      $("#count-anotations").text(
        $(".container-anotacions").find(".annotator-marginviewer-element")
          .length
      );
    };

    AnnotatorViewer.prototype.onAnnotationReply = function (annotation) {
      $("li").remove("#annotation-" + annotation.id);
      $("#count-anotations").text(
        $(".container-anotacions").find(".annotator-marginviewer-element")
          .length
      );
    };

    AnnotatorViewer.prototype.onAnnotationCollapse = function (annotation) {
      alert("Aqui si llego");
    };

    AnnotatorViewer.prototype.mascaraAnnotation = function (annotation) {
      if (!annotation.data_creacio) annotation.data_creacio = $.now();

      //Obtener el usuario:
      //console.log($("#usuarioConectado").text());

      //Verifico los permisos:

      // var currentUser = sessionStorage.getItem("user");

      var currentUser = document
        .getElementById("databackend")
        .getAttribute("currentuser");

      //alert(currentUser);

      updatePermission = annotation.permissions.update.includes(currentUser);
      deletePermission = annotation.permissions.delete.includes(currentUser);
      replyPermission = true;

      if (currentUser == "Anonymous") {
        replyPermission = false;
      }

      //console.log(updatePermission);
      //console.log(deletePermission);

      var shared_annotation = "";
      var class_label = "label";

      var delete_icon = "";

      if (annotation.category != "reply") {
        if (deletePermission) {
          delete_icon =
            '<img src="' +
            IMAGE_DELETE +
            '" class="annotator-viewer-delete" title="' +
            i18n_dict.Delete +
            '" style=" float:right;margin-top:3px;;margin-left:3px"/>';
        }

        var pathOrigen = document
          .getElementById("databackend")
          .getAttribute("basepath");

        var edit_icon = "";
        editTxt = i18n_dict.Edit;
        if (updatePermission) {
          edit_icon =
            '<img src="' +
            pathOrigen +
            '/static/src/img/edit-icon.png"  ' +
            `class="annotator-viewer-edit" title="${editTxt}" style="float:right;margin-top:3px"/>`;
        }

        delete_icon = delete_icon + edit_icon;
      } else {
        if (deletePermission) {
          var delete_icon =
            '<img src="' +
            IMAGE_DELETE +
            '" class="annotator-viewer-delete" title="' +
            i18n_dict.Delete +
            '" style=" float:right;margin-top:3px;;margin-left:3px"/>';
        }
      }

      var reply_icon =
        '<img src="' +
        IMAGE_REPLY +
        '" class="annotator-viewer-reply" title="' +
        i18n_dict.Reply +
        '" style=" float:right;margin-top:3px;;margin-left:3px"/>';

      if (!replyPermission) {
        reply_icon = "";
      }

      var like_icon = "";
      likeTxt = i18n_dict.Like;

      //Obtengo el valor del like.

      estadosAnnotation = annotation["statechanges"];

      likethisAnnotation = false;

      if (estadosAnnotation) {
        for (let i = 0; i < estadosAnnotation.length; i++) {
          if (
            estadosAnnotation[i]["objtype"] == "annotation_like" &&
            estadosAnnotation[i]["user"] == currentUser
          ) {
            likethisAnnotation = true;
          }
        }
      }

      if (replyPermission) {
        if (likethisAnnotation) {
          like_icon = `<i style="float: right;margin-top:10px;margin-left:3px;" class="fa-solid fa-heart  fa-lg annotator-viewer-like"></i>`;
        } else {
          like_icon = `<i style="float: right;margin-top:10px;margin-left:3px;" class="fa-regular fa-heart  fa-lg annotator-viewer-like"></i>`;
        }
      }

      if (annotation.estat == 1 || annotation.permissions.read.length === 0) {
        shared_annotation =
          '<img src="' +
          SHARED_ICON +
          '" title="' +
          i18n_dict.share +
          '" style="margin-left:5px"/>';
      }

      if (annotation.propietary == 0) {
        class_label = "label-compartit";
        delete_icon = "";
      }

      //If you have instal.led a plug-in for categorize anotations, panel viewer can get this information with the category atribute
      if (annotation.category != null) {
        anotation_color = annotation.category;
      } else {
        anotation_color = "hightlight";
      }

      var textAnnotation = annotation.text;

      if (annotation.category == "reply") {
        //Format the box if is a reply:

        var annotation_text2 =
          '<div class="replyDetail">' +
          '<div style="">' +
          '<span style="font-weight: 700;">' +
          annotation.user.split("@", 1) +
          // " id: " +
          // annotation.id +
          // " aRep: " +
          // annotation.idAnotationReply +
          "</span>" +
          "   (" +
          $.format.date(annotation.data_creacio, "MM/yyyy HH:mm") +
          ")" +
          '<div style="width: 160px;height: 2px;border-bottom: 1px solid #d4d4d4;position: relative;" class="line"></div>' +
          "</div>" +
          '<div style="">' +
          textAnnotation + //'Me parece que este comentario esta fuera de su lugar. No solamente no toma en cuenta el estandar si no que ademas esta dentro de otro problema de investigacion.'+
          "</div>" +
          "</div>";
        //Inserto tantas lineas como niveles de profundidad

        textoLineasNiveles =
          '<div style="border-radius: 3px;flex-basis:3px;background-color:#d4d4d4;width:3.58px;"puch ></div>'.repeat(
            annotation.level
          );

        var annotation_layer1 =
          '<div id="cont-' +
          annotation.id +
          '"  style="align-self:end;min-height:18px;grid-template-columns: repeat(1,2fr);width:50px;min-width: 50px;background-color: #f5f5f5;">' +
          //'<span id="nrep-'+annotation.id+'"> </span>' +
          '<button  id="nrep-' +
          annotation.id +
          '" type="button" class="annotator-viewer-collapse btn  anotator_chevron_button isexpand" style="border-width: 0px; background-color: transparent;  min-height: 27px;"  ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path><path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"></path></svg></button> ' +
          "</div>" +
          '<div class="flex-replyBox">' +
          //'<div style="border-radius: 3px;flex-basis:3px;background-color:#d4d4d4;width:3.58px;" ></div>'+
          textoLineasNiveles +
          '<div style="border:0px;flex-grow:4;">' +
          annotation_text2 +
          "</div>" +
          "</div>";
        var annotation_layer =
          '<div class="flex-replyContainer" style="background-color: #f5f5f5;width:100%" idannotationref="' +
          annotation.idAnotationReply +
          '">' +
          annotation_layer1 +
          '<div class="annotator-marginviewer-footer">' +
          shared_annotation +
          delete_icon +
          reply_icon +
          like_icon +
          "</div>" +
          '<div class="annotator-marginviewer-reply">' +
          '<div class="anotador_text">' +
          "" +
          "</div>" +
          "</div>" +
          "</div>";

        /*var annotation_layer =
        '<div class="annotator-marginviewer-text">'+
        '<div class="' +
        anotation_color +
        ' anotator_color_box"></div>';
      annotation_layer +=
        '<div class="anotador_text">' +
        textAnnotation +
        '</div></div><div class="annotator-marginviewer-date">' +
        $.format.date(annotation.data_creacio, "dd/MM/yyyy HH:mm:ss") +
        '</div><div class="annotator-marginviewer-quote">' +
        annotation.quote +
        '</div><div class="annotator-marginviewer-footer"><span class="' +
        class_label +
        '">' +
        annotation.user +
        "</span>" +
        shared_annotation +
        delete_icon +
        reply_icon 
        +
        "</div>"+
        '<div class="annotator-marginviewer-reply">' +
            '<div class="anotador_text">' +
            "" +
            '</div>'+
        '</div>'
        ;*/
      } else {
        var annotation_layer =
          '<div class="annotator-marginviewer-text">' +
          '<div  style="display: flex;width:100%;min-width:100%;">' +
          '<div class="' +
          anotation_color +
          ' anotator_color_box"> ' +
          "</div>" +
          '<button id="nrep-' +
          annotation.id +
          '" type="button" class="annotator-viewer-collapse btn  anotator_chevron_button isexpand" style="border-width: 0px; background-color: transparent;"  ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path><path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"></path></svg></button>' +
          "</div>";
        var annotation_stateCode = annotation.state;
        var annotation_stateSpan = "";
        if (annotation_stateCode == 2) {
          annotation_stateSpan =
            '<span class="' +
            class_label +
            '" style="color:#98218c;">' +
            "Aprobado" +
            "</span>";
        }

        annotation_layer +=
          '<div class="anotador_ident">' +
          "</div>" +
          '<div style="width: 160px;height: 2px;max-width: 2px !important;border-bottom: 1px solid #d4d4d4;position: relative;" class="line"></div>' +
          '<div class="anotador_text">' +
          textAnnotation +
          "</div>" +
          "</div>" +
          '<div class="annotator-marginviewer-date">' +
          $.format.date(annotation.data_creacio, "dd/MM/yyyy HH:mm:ss") +
          "</div>" +
          '<!--<div class="area-of-interest" id="timecont-' +
          annotation.id +
          '" >' +
          'Interaction: <span id="time-annotation-' +
          annotation.id +
          '"></span> seconds.' +
          "</div> -->" +
          '<div class="annotator-marginviewer-quote">' +
          annotation.quote +
          '</div><div class="annotator-marginviewer-footer">' +
          '<span class="' +
          class_label +
          '">' +
          annotation.user.split("@", 1) +
          "</span>" +
          annotation_stateSpan +
          shared_annotation +
          delete_icon +
          reply_icon +
          like_icon +
          "</div>" +
          '<div class="annotator-marginviewer-reply">' +
          '<div class="anotador_text">' +
          "" +
          "</div>" +
          "</div>";
      }

      return annotation_layer;
    };

    AnnotatorViewer.prototype.createAnnotationPanel = function (annotation) {
      myAnotationTxt = i18n_dict.my_annotations;
      sharedTxt = i18n_dict.Shared;

      var checboxes = `<label class="checkbox-inline"><input type="checkbox" id="type_own" rel="meAnotator"/>${myAnotationTxt}</label><label class="checkbox-inline">`; //  <input type="checkbox" id="type_share" rel="shared"/>${sharedTxt}</label>`;

      var annotation_layer =
        '<div  class="annotations-list-uoc" ><div id="annotations-panel"><span class="rotate etiquetaSolapa" title="' +
        i18n_dict.view_annotations +
        " " +
        i18n_dict.pdf_resum +
        '" >' +
        i18n_dict.view_annotations +
        '<span class="label-counter" style="padding:0.2em 0.3em;float:right" id="count-anotations">0</span></span></div><div id="anotacions-uoc-panel" style="height:80%"><ul class="container-anotacions"><li class="filter-panel">' +
        checboxes +
        "</li></ul></div></div>";

      return annotation_layer;
    };

    AnnotatorViewer.prototype.createReferenceAnnotation = function (
      annotation
    ) {
      var anotation_reference = null;
      var anotation_link = null;
      var data_owner = "meAnotator";
      var data_type = "";
      var myAnnotation = false;

      if (annotation.id != null) {
        anotation_reference = "annotation-" + annotation.id;
        anotation_link = annotation.idAnotationReply;
      } else {
        annotation.id = this.uniqId();
        //We need to add this id to the text anotation
        $element = $("span.annotator-hl:not([id])");
        if ($element) {
          $element.prop("id", annotation.id);
        }
        anotation_reference = "annotation-" + annotation.id;
      }

      if (annotation.estat == 1 || annotation.permissions.read.length === 0) {
        data_type = "shared";
      }
      if (annotation.propietary == 0) {
        data_owner = "";
      } else {
        myAnnotation = true;
      }

      //var currentUser = sessionStorage.getItem("user");

      var currentUser = document
        .getElementById("databackend")
        .getAttribute("currentuser");

      if (annotation.user == currentUser) {
        data_owner = "meAnotator";
      } else {
        data_owner = "";
      }

      var annotation_layer =
        '<li class="annotator-marginviewer-element ' +
        data_type +
        " " +
        data_owner +
        '" id="' +
        anotation_reference +
        '"' +
        '" idlink="' +
        anotation_link +
        '"' +
        ">" +
        this.mascaraAnnotation(annotation) +
        "</li>";
      var malert = i18n_dict.anotacio_lost;

      if (annotation.idAnotationReply != null) {
        //Aqui busco si es un reply y lo inserto debajo de su referencia.

        anotacioObject = $(annotation_layer)
          .insertAfter("#" + annotation.idAnotationReply)
          .click(function (event) {
            var viewPanelHeight = jQuery(window).height();
            var annotation_reference = annotation.id;

            $element = jQuery("#" + annotation.id);
            if (!$element.length) {
              $element = jQuery("#" + annotation.order);
              annotation_reference = annotation.order; //If exists a sorted annotations we put it in the right order, using order attribute
            }

            if ($element.length) {
              elOffset = $element.offset();
              $(this).children(".annotator-marginviewer-quote").toggle();
              $("html, body").animate(
                {
                  scrollTop:
                    $("#" + annotation_reference).offset().top -
                    viewPanelHeight / 2,
                },
                2000
              );
            }
          })
          .mouseover(function () {
            $element = jQuery("span[id=" + annotation.id + "]");
            if ($element.length) {
              $element.css({
                "border-color": "#000000",
                "border-width": "1px",
                "border-style": "solid",
              });
            }
          })
          .mouseout(function () {
            $element = jQuery("span[id=" + annotation.id + "]");
            if ($element.length) {
              $element.css({
                "border-width": "0px",
              });
            }
          });
      } else {
        //Caso contrario inserto al final de la lista.

        anotacioObject = $(annotation_layer)
          .appendTo(".container-anotacions")
          .click(function (event) {
            var viewPanelHeight = jQuery(window).height();
            var annotation_reference = annotation.id;

            $element = jQuery("#" + annotation.id);
            if (!$element.length) {
              $element = jQuery("#" + annotation.order);
              annotation_reference = annotation.order; //If exists a sorted annotations we put it in the right order, using order attribute
            }

            if ($element.length) {
              elOffset = $element.offset();
              //$(this).children(".annotator-marginviewer-quote").toggle();
              $("html, body").animate(
                {
                  scrollTop:
                    $("#" + annotation_reference).offset().top -
                    viewPanelHeight / 2,
                },
                2000
              );
            }
          })
          .mouseover(function () {
            $element = jQuery("span[id=" + annotation.id + "]");
            if ($element.length) {
              $element.css({
                "border-color": "#000000",
                "border-width": "1px",
                "border-style": "solid",
              });
            }
          })
          .mouseout(function () {
            $element = jQuery("span[id=" + annotation.id + "]");
            if ($element.length) {
              $element.css({
                "border-width": "0px",
              });
            }
          });
      }

      //Adding annotation to data element for delete and link
      $("#" + anotation_reference).data("annotation", annotation);
      $(anotacioObject).fadeIn("fast");
    };

    AnnotatorViewer.prototype.uniqId = function () {
      return Math.round(new Date().getTime() + Math.random() * 100);
    };

    //Strip content tags
    AnnotatorViewer.prototype.removeTags = function (striptags, html) {
      striptags = (
        ((striptags || "") + "").toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []
      ).join("");
      var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi,
        commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi;

      return html
        .replace(commentsAndPhpTags, "")
        .replace(tags, function ($0, $1) {
          return html.indexOf("<" + $1.toLowerCase() + ">") > -1 ? $0 : "";
        });
    };

    return AnnotatorViewer;
  })(Annotator.Plugin);
}).call(this);
