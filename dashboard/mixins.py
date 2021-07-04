from django.http.response import JsonResponse


class AjaxFormMixin(object):
    
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
        
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        # print(form.cleaned_data)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'Succesfully submitted data'
            }
            return JsonResponse(data)
        else:
            return response