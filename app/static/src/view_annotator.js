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
      ".annotator-viewer-delete click": "onDeleteClick",
      ".annotator-viewer-edit click": "onEditClick",
      ".annotator-viewer-reply click": "onReplyClick",
      ".annotator-viewer-delete mouseover": "onDeleteMouseover",
      ".annotator-viewer-delete mouseout": "onDeleteMouseout",
      ".annotator-viewer-reply mouseover": "onReplyMouseover",
      ".annotator-viewer-reply mouseout": "onReplyMouseout",
    };

    AnnotatorViewer.prototype.field = null;

    AnnotatorViewer.prototype.input = null;

    AnnotatorViewer.prototype.options = {
      AnnotatorViewer: {},
    };

    function AnnotatorViewer(element, options) {
      this.onAnnotationCreated = __bind(this.onAnnotationCreated, this);
      this.onAnnotationUpdated = __bind(this.onAnnotationUpdated, this);
      this.onDeleteClick = __bind(this.onDeleteClick, this);
      this.onEditClick = __bind(this.onEditClick, this);
      this.onDeleteMouseover = __bind(this.onDeleteMouseover, this);
      this.onDeleteMouseout = __bind(this.onDeleteMouseout, this);

      this.onReplyClick = __bind(this.onReplyClick, this);
      this.onReplyMouseover = __bind(this.onReplyMouseover, this);
      this.onReplyMouseout = __bind(this.onReplyMouseout, this);

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

      if (type == "delete") {
        return this.annotator.deleteAnnotation(item.data("annotation"));
      }
      if (type == "reply") {
        //console.log("Ha entrado en la accion de reply");

        var annotator_textArea = item.find("div.annotator-marginviewer-reply");
        annotator_textArea = annotator_textArea.find("div.anotador_text");

        //Obtengo los valores:
        idReferencia = annotator_textArea.prevObject.prevObject[0].id;
        item.id = idReferencia.split("-")[1];

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

      /*let annotator_textArea=item.find("div.anotador_text");
        this.textareaEditor(annotator_textArea,item.data("annotation"))*/
      //this.annotator.replyAnnotation(item.data("annotation"));

      if (type == "edit") {
        //console.log("Ha entrado en la accion de edit");

        var annotator_textArea = item.find("div.annotator-marginviewer-text");
        annotator_textArea = annotator_textArea.find("div.anotador_text");

        //Obtengo los valores:
        idReferencia = annotator_textArea.prevObject.prevObject[0].id;
        item.id = idReferencia.split("-")[1];

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
        $('<a href="#save" class="annotator-panel-save">Save</a>')
          .appendTo(control_buttons)
          .bind("click", { annotation: item }, this.onSavePanel);
        $('<a href="#cancel" class="annotator-panel-cancel">Cancel</a>')
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
      item.id = idReferencia.split("-")[1];

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
            "Texto to Reply..." +
            "</textarea>"
        );

        if (item.category == "reply") {
          var annotationCSSReference =
            "li#annotation-" +
            item.id +
            "> div.flex-replyContainer > div.annotator-marginviewer-reply";
        } else {
          var annotationCSSReference =
            "li#annotation-" + item.id + " > div.annotator-marginviewer-reply";
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
        $('<a href="#save" class="annotator-panel-save">Save</a>')
          .appendTo(control_buttons)
          .bind("click", { annotation: item }, this.onSavePanelReply);
        $('<a href="#cancel" class="annotator-panel-cancel">Cancel</a>')
          .appendTo(control_buttons)
          .bind("click", { annotation: item }, this.onCancelPanelReply);
      }
    };

    AnnotatorViewer.prototype.tinymceActivation = function (selector) {
      tinymce.init({
        selector: selector,
        plugins: "media image insertdatetime link paste",
        menubar: false,
        statusbar: false,
        toolbar_items_size: "small",
        extended_valid_elements: "",
        toolbar:
          "undo redo bold italic alignleft aligncenter alignright alignjustify | link image media",
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
        tinymce.remove("#textarea-" + current_annotation.id);
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
        tinymce.remove("#textareaReply-" + current_annotation.id);
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
      anotacionReply.user = "Me";
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
        tinymce.remove("#textarea-" + current_annotation.id);

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
        tinymce.remove("#textareaReply-" + current_annotation.id);

        var textAnnotation =
          '<div class="anotador_text" ' + styleHeight + ">" + "" + "</div>";

        var anotacio_capa =
          '<div class="annotator-marginviewer-reply">' +
          textAnnotation +
          "</div>";

        if (current_annotation.category == "reply") {
          var textAreaEditorReply = $(
            "li#annotation-" +
              current_annotation.id +
              " > .flex-replyContainer > .annotator-marginviewer-reply"
          );
        } else {
          var textAreaEditorReply = $(
            "li#annotation-" +
              current_annotation.id +
              " > .annotator-marginviewer-reply"
          );
        }

        textAreaEditorReply.replaceWith(anotacio_capa);
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
        /*let textoAnotacion=valor.children[0].children[1].innerHTML
        let textoCortado=textoAnotacion.substring(0, textoAnotacion.length-4)
        let strippedCortadoText = textoCortado.replace(/<[^>]+>/g, '');
        let strippedAnnotation =annotation.text.replace(/<[^>]+>/g, '');
        if(strippedAnnotation.startsWith(strippedCortadoText)){
          $("li").remove("#" + anotacionId);
        }*/
        /*if( textoAnotacion==annotation.text){
          $("li").remove("#" + anotacionId);

        }*/
      });
      if (annotation.id != null) {
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

    AnnotatorViewer.prototype.mascaraAnnotation = function (annotation) {
      if (!annotation.data_creacio) annotation.data_creacio = $.now();

      //Obtener el usuario:
      //console.log($("#usuarioConectado").text());

      //Verifico los permisos:

      var currentUser = sessionStorage.getItem("user");
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
        if (updatePermission) {
          edit_icon =
            '<img src="' +
            pathOrigen +
            '/static/src/img/edit-icon.png"  ' +
            'class="annotator-viewer-edit" title="Edit" style="float:right;margin-top:3px"/>';
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
          "</span>" +
          "   (" +
          $.format.date(annotation.data_creacio, "MM/yyyy HH:mm") +
          ")" +
          "</br>IdRef:" +
          annotation.idAnotationReply.split("-")[1] +
          "</br>IdRoot:" +
          annotation.idReplyRoot +
          "</br>" +
          "Id:" +
          annotation.id +
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
          '<div class="flex-replyBox">' +
          //'<div style="border-radius: 3px;flex-basis:3px;background-color:#d4d4d4;width:3.58px;" ></div>'+
          textoLineasNiveles +
          '<div style="border:0px;flex-grow:4;">' +
          annotation_text2 +
          "</div>" +
          "</div>";
        var annotation_layer =
          '<div class="flex-replyContainer">' +
          annotation_layer1 +
          '<div class="annotator-marginviewer-footer">' +
          shared_annotation +
          delete_icon +
          reply_icon +
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
          '<div class="' +
          anotation_color +
          ' anotator_color_box"></div>';
        annotation_layer +=
          '<div class="anotador_ident">' +
          "Id:" +
          annotation.id +
          "</div>" +
          '<div style="width: 160px;height: 2px;border-bottom: 1px solid #d4d4d4;position: relative;" class="line"></div>' +
          '<div class="anotador_text">' +
          textAnnotation +
          "</div>" +
          '</div><div class="annotator-marginviewer-date">' +
          $.format.date(annotation.data_creacio, "dd/MM/yyyy HH:mm:ss") +
          '</div><div class="annotator-marginviewer-quote">' +
          annotation.quote +
          '</div><div class="annotator-marginviewer-footer"><span class="' +
          class_label +
          '">' +
          annotation.user.split("@", 1) +
          "</span>" +
          shared_annotation +
          delete_icon +
          reply_icon +
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
      var checboxes =
        '<label class="checkbox-inline"><input type="checkbox" id="type_own" rel="me"/>My annotations</label><label class="checkbox-inline">  <input type="checkbox" id="type_share" rel="shared"/>Shared</label>';

      var annotation_layer =
        '<div  class="annotations-list-uoc" style="background-color:#ddd;"><div id="annotations-panel"><span class="rotate" title="' +
        i18n_dict.view_annotations +
        " " +
        i18n_dict.pdf_resum +
        '" style="padding:5px;background-color:#ddd;position: absolute; top:10em;left: -50px; width: 155px; height: 110px;cursor:pointer">' +
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
      var data_owner = "me";
      var data_type = "";
      var myAnnotation = false;

      if (annotation.id != null) {
        anotation_reference = "annotation-" + annotation.id;
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

      var currentUser = sessionStorage.getItem("user");

      if (annotation.user == currentUser) {
        data_owner = "me";
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
        '">' +
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
}.call(this));
