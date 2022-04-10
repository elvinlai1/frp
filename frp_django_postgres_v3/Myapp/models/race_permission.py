from django.forms import models


class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        #权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的
        permissions = (
            ('views_work_list', '查看工作信息表'),
            ('views_user_info', '查看用户信息'),
        )