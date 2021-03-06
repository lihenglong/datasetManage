# Generated by Django 2.2 on 2021-02-20 11:41

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='逻辑删除')),
                ('local_path', models.CharField(default='', max_length=511, verbose_name='本地路径')),
                ('oss_path', models.CharField(default='', max_length=511, verbose_name='oss路径')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
            ],
            options={
                'verbose_name': '图片表',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='逻辑删除')),
                ('value', models.CharField(default='', max_length=511, verbose_name='类别')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='image.Category')),
            ],
            options={
                'verbose_name': '分类表',
            },
        ),
    ]
