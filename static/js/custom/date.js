/**
 * Created by alexy on 28.05.15.
 */
$(function() {
  $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
  );
  $("#js-surface-photo-add-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-surface-photo-update-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $(".start_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $(".end_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-surface-add-client-form #id_date_start").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-surface-add-client-form #id_date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-maket-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-update-maket-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-order-form #id_date_start").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-order-form #id_date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-update-order-form #id_date_start").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-update-order-form #id_date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-surface-form #date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-surface-form #date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-city-form #id_contract_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-client_task-add-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-client_task-update-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-task-add-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-address-filter-form #id_a_date_s").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-address-filter-form #id_a_date_e").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-task-filter-form #id_date_s").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-task-filter-form #id_date_e").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-journal-filter-date_e").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-journal-filter-date_s").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-form-incomingtask-add").find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-form-incomingtask-update").find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-incomingtask-search-form").find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $("#js-incomingtask-search-form").find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });

});