#include "hpy.h"

typedef struct {
  HPyObject_HEAD
  /* Type-specific fields go here. */
  double *data;
  int size;
} ArrayObject;

HPyDef_SLOT(Array_destroy, Array_destroy_impl, HPy_tp_destroy)
static void Array_destroy_impl(void *obj) {
  ArrayObject *self = (ArrayObject *)obj;
  free(self->data);
}

HPyDef_SLOT(Array_init, Array_init_impl, HPy_tp_init)
static int Array_init_impl(HPyContext ctx, HPy h_self, HPy *args,
                           HPy_ssize_t nargs, HPy kw) {
  static const char *kwlist[] = {"data", NULL};
  ArrayObject *self = HPy_CAST(ctx, ArrayObject, h_self);
  int index;
  HPy h_data = HPy_NULL;
  HPyTracker ht;
  if (!HPyArg_ParseKeywords(ctx, &ht, args, nargs, kw, "|O", kwlist, &h_data))
    return -1;

  if (!HPyList_Check(ctx, h_data)) {
    HPyErr_SetString(ctx, ctx->h_TypeError, "parameter must be a list");
    return -1;
  }

  self->size = (int)HPy_Length(ctx, h_data);

  self->data = (double *)malloc(self->size * sizeof(double));
  if (self->data == NULL) {
    HPyErr_NoMemory(ctx);
    return -1;
  }

  // XXX: this is not doing any error check (but the original C-API version
  // doesn't either :shrug:
  for (index = 0; index < self->size; index++) {
    HPy h_item = HPy_GetItem_i(ctx, h_data, index);
    self->data[index] = HPyFloat_AsDouble(ctx, h_item);
    HPy_Close(ctx, h_item);
  }

  return 0;
}

HPyDef_MEMBER(Array_size, "size", HPyMember_INT, offsetof(ArrayObject, size),
              .doc = "size of the array")

HPyDef_METH(Array_tolist, "tolist", Array_tolist_impl, HPyFunc_NOARGS,
            .doc = "Return the data as a list")
static HPy Array_tolist_impl(HPyContext ctx, HPy h_self) {
  ArrayObject *self = HPy_CAST(ctx, ArrayObject, h_self);
  int index;
  HPyListBuilder builder = HPyListBuilder_New(ctx, self->size);
  for (index = 0; index < self->size; index++) {
    HPy h_item = HPyFloat_FromDouble(ctx, self->data[index]);
    HPyListBuilder_Set(ctx, builder, index, h_item);
    HPy_Close(ctx, h_item);
  }
  return HPyListBuilder_Build(ctx, builder);
};

static HPy Array_empty(HPyContext ctx, int size, ArrayObject **result);

HPyDef_SLOT(Array_multiply, Array_multiply_impl, HPy_nb_multiply)
static HPy Array_multiply_impl(HPyContext ctx, HPy h1, HPy h2) {
  int index;
  double number;
  HPy h_number = HPy_NULL;
  ArrayObject *result = NULL, *arr = NULL;
  HPy h_result = HPy_NULL;

  if (HPyNumber_Check(ctx, h2)) {
    h_number = h2;
    arr = HPy_CAST(ctx, ArrayObject, h1);
  } else if (HPyNumber_Check(ctx, h1)) {
    h_number = h1;
    arr = HPy_CAST(ctx, ArrayObject, h2);
  }

  if (HPyNumber_Check(ctx, h1) || HPyNumber_Check(ctx, h2)) {
    number = HPyFloat_AsDouble(ctx, h_number);
    h_result = Array_empty(ctx, arr->size, &result);
    for (index = 0; index < arr->size; index++) {
      result->data[index] = arr->data[index] * number;
    }
  }
  /* XXX exception if result is still NULL here */
  return h_result;
};

HPyDef_SLOT(Array_add, Array_add_impl, HPy_nb_add)
static HPy Array_add_impl(HPyContext ctx, HPy h1, HPy h2) {
  int index;
  ArrayObject *result = NULL, *a1, *a2;
  HPy h_result = HPy_NULL;
  a1 = HPy_CAST(ctx, ArrayObject, h1);
  a2 = HPy_CAST(ctx, ArrayObject, h2);

  if (a1->size != a2->size)
    return HPy_NULL;   /* XXX should raise an exception */

  h_result = Array_empty(ctx, a1->size, &result);
  for (index = 0; index < a1->size; index++) {
    result->data[index] = a1->data[index] + a2->data[index];
  }
  return h_result;
};

HPyDef_SLOT(Array_divide, Array_divide_impl, HPy_nb_true_divide)
static HPy Array_divide_impl(HPyContext ctx, HPy h1, HPy h2) {
  int index;
  double number;
  ArrayObject *result = NULL, *a1;
  HPy h_result = HPy_NULL;

  if (!HPyNumber_Check(ctx, h2)) {
    return HPy_NULL;
  }
  a1 = HPy_CAST(ctx, ArrayObject, h1);
  number = HPyFloat_AsDouble(ctx, h2);
  h_result = Array_empty(ctx, a1->size, &result);
  for (index = 0; index < a1->size; index++) {
    result->data[index] = a1->data[index] / number;
  }
  return h_result;
};


HPyDef_SLOT(Array_length, Array_length_impl, HPy_sq_length)
HPy_ssize_t Array_length_impl(HPyContext ctx, HPy h_arr) {
  ArrayObject *arr = HPy_CAST(ctx, ArrayObject, h_arr);
  HPy_ssize_t result = (HPy_ssize_t)arr->size;
  return result;
};


HPyDef_SLOT(Array_item, Array_item_impl, HPy_sq_item)
HPy Array_item_impl(HPyContext ctx, HPy h_arr, HPy_ssize_t index) {
  ArrayObject *arr = HPy_CAST(ctx, ArrayObject, h_arr);
  if (index < 0 || index >= arr->size) {
    HPyErr_SetString(ctx, ctx->h_IndexError, "index out of range");
    return HPy_NULL;
  }
  HPy item = HPyFloat_FromDouble(ctx, arr->data[index]);
  return item;
};

HPyDef_SLOT(Array_setitem, Array_setitem_impl, HPy_sq_ass_item)
int Array_setitem_impl(HPyContext ctx, HPy h_arr, HPy_ssize_t index, HPy h_item) {
  ArrayObject *arr = HPy_CAST(ctx, ArrayObject, h_arr);
  if (index < 0 || index >= arr->size) {
    HPyErr_SetString(ctx, ctx->h_IndexError, "index out of range");
    return -1;
  }
  double value = HPyFloat_AsDouble(ctx, h_item);
  if (HPyErr_Occurred(ctx))
    return -1;
  arr->data[index] = value;
  return 0;
};


HPyDef_SLOT(Array_new, HPyType_GenericNew, HPy_tp_new)

static HPyDef *Array_defines[] = {
    // slots
    &Array_new,
    &Array_init,
    &Array_destroy,
    &Array_add,
    &Array_multiply,
    &Array_divide,
    &Array_item,
    &Array_setitem,
    &Array_length,
    // members
    &Array_size,
    // methods
    &Array_tolist,
    NULL
};

static HPyType_Spec Array_type_spec = {
    .name = "_piconumpy_hpy.array",
    .basicsize = sizeof(ArrayObject),
    .itemsize = 0,
    .flags = HPy_TPFLAGS_DEFAULT,
    .defines = Array_defines,
};

HPy h_ArrayType;

static HPy Array_empty(HPyContext ctx, int size, ArrayObject **result) {
  ArrayObject *new_array;
  HPy h_new_array = HPy_New(ctx, h_ArrayType, &new_array);
  new_array->size = size;
  new_array->data = (double *)malloc(size * sizeof(double));
  if (new_array->data == NULL) {
     return HPyErr_NoMemory(ctx);
  }
  *result = new_array;
  return h_new_array;
};

HPyDef_METH(empty, "empty", empty_impl, HPyFunc_O, .doc = "Create an empty array")
static HPy empty_impl(HPyContext ctx, HPy module, HPy arg) {
  int size;
  ArrayObject *result;
  size = (int)HPyLong_AsLong(ctx, arg);
  return Array_empty(ctx, size, &result);
};

HPyDef_METH(zeros, "zeros", zeros_impl, HPyFunc_O, .doc = "Create a zero-filled array")
static HPy zeros_impl(HPyContext ctx, HPy module, HPy arg) {
  int size;
  ArrayObject *result;
  size = (int)HPyLong_AsLong(ctx, arg);
  HPy h_result = Array_empty(ctx, size, &result);
  if (HPy_IsNull(h_result))
      return HPy_NULL;
  for(int i=0; i<size; i++)
      result->data[i] = 0;
  return h_result;
};


static HPyDef *module_defines[] = {
    &empty,
    &zeros,
    NULL
};

static HPyModuleDef piconumpymodule = {
    HPyModuleDef_HEAD_INIT,
    .m_name = "_piconumpy_hpy",
    .m_doc = "piconumpy implemented with the HPy API.",
    .m_size = -1,
    .defines = module_defines,
};

HPy_MODINIT(_piconumpy_hpy)
static HPy init__piconumpy_hpy_impl(HPyContext ctx) {
  HPy hm = HPyModule_Create(ctx, &piconumpymodule);
  if (HPy_IsNull(hm))
    return HPy_NULL;

  h_ArrayType = HPyType_FromSpec(ctx, &Array_type_spec, NULL);
  if (HPy_IsNull(h_ArrayType))
      return HPy_NULL;

  if (HPy_SetAttr_s(ctx, hm, "array", h_ArrayType) < 0) {
    HPy_Close(ctx, h_ArrayType);
    HPy_Close(ctx, hm);
    return HPy_NULL;
  }

  return hm;
}
