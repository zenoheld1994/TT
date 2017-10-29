var Login = function() {
    var e = function() {
        $(".login-form").validate({
            errorElement: "span",
            errorClass: "help-block",
            focusInvalid: !1,
            rules: {
                school_name: {
                    required: !0
                },
                username: {
                    required: !0
                },
                password: {
                    required: !0
                },
                remember: {
                    required: !1
                }
            },
            messages: {
                school_name: {
                    required: "El nombre de la escuela es requerido."
                },
                username: {
                    required: "El usuario es requerido."
                },
                password: {
                    required: "La contraseña es requerida."
                }
            },
            invalidHandler: function(e, r) {
                $(".alert-danger", $(".login-form")).show();
            },
            highlight: function(e) {
                $(e).closest(".form-group").addClass("has-error");
            },
            success: function(e) {
                e.closest(".form-group").removeClass("has-error"), e.remove();
            },
            errorPlacement: function(e, r) {
                e.insertAfter(r.closest(".input-icon"));
            },
            submitHandler: function(e) {
                e.submit();
            }
        }), $(".login-form input").keypress(function(e) {
            return 13 == e.which ? ($(".login-form").validate().form() && $(".login-form").submit(), 
            !1) : void 0;
        });
    };
    return {
        init: function() {
            e();
        }
    };
}();

jQuery(document).ready(function() {
    Login.init();
});