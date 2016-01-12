# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ligand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuxProtein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('uniprot_id', models.CharField(max_length=20)),
                ('sequence', models.TextField(null=True)),
                ('deletions', models.TextField(max_length=100, null=True)),
                ('position', models.TextField(max_length=20, null=True)),
                ('remarks', models.TextField(null=True)),
            ],
            options={
                'db_table': 'construct_aux_protein',
            },
        ),
        migrations.CreateModel(
            name='AuxProteinType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'construct_aux_protein_type',
            },
        ),
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'construct_chemical',
            },
        ),
        migrations.CreateModel(
            name='ChemicalConc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentration', models.TextField(null=True)),
            ],
            options={
                'db_table': 'construct_chemical_conc',
            },
        ),
        migrations.CreateModel(
            name='ChemicalList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'construct_chemical_list',
            },
        ),
        migrations.CreateModel(
            name='ChemicalModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'construct_chemical_modification',
            },
        ),
        migrations.CreateModel(
            name='ChemicalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'construct_chemical_type',
            },
        ),
        migrations.CreateModel(
            name='Construct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deletions', models.TextField(max_length=100, null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='construct.Construct')),
            ],
            options={
                'db_table': 'construct',
            },
        ),
        migrations.CreateModel(
            name='ConstructCrystallization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.TextField(max_length=100, null=True)),
                ('settings', models.TextField(max_length=100, null=True)),
                ('remarks', models.TextField(max_length=1000, null=True)),
                ('protein_conc', models.SlugField(blank=True, max_length=20)),
                ('aqueous_solution_lipid_ratio', models.SlugField(max_length=20, null=True)),
                ('lcp_bolus_volume', models.SlugField(max_length=20, null=True)),
                ('precipitant_solution_volume', models.SlugField(max_length=20, null=True)),
                ('temp', models.CharField(max_length=5, null=True)),
                ('ph', models.TextField(max_length=10, null=True)),
                ('chemical_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.ChemicalList')),
                ('construct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.Construct')),
            ],
            options={
                'db_table': 'construct_crystallization',
            },
        ),
        migrations.CreateModel(
            name='ConstructCrystallizationLigandConc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ligand_conc', models.TextField(null=True)),
                ('construct_crystallization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.ConstructCrystallization')),
                ('ligand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligand.Ligand')),
            ],
            options={
                'db_table': 'construct_ligand_conc_of_crystallization',
            },
        ),
        migrations.CreateModel(
            name='ConstructExpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(null=True)),
                ('construct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.Construct')),
            ],
            options={
                'db_table': 'construct_expression',
            },
        ),
        migrations.CreateModel(
            name='ConstructExpressionSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression_method', models.CharField(max_length=100)),
                ('host_cell_type', models.CharField(max_length=100)),
                ('host_cell', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'construct_expression_system',
            },
        ),
        migrations.CreateModel(
            name='ConstructPurification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(null=True)),
                ('construct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.Construct')),
            ],
            options={
                'db_table': 'construct_purification',
            },
        ),
        migrations.CreateModel(
            name='ConstructSolubilization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(null=True)),
                ('chemical_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.ChemicalList')),
                ('construct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.Construct')),
            ],
            options={
                'db_table': 'construct_solubilization',
            },
        ),
        migrations.CreateModel(
            name='CrystallizationMethodTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'construct_crystallization_method_types',
            },
        ),
        migrations.CreateModel(
            name='PurificationStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('purification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.ConstructPurification')),
            ],
            options={
                'db_table': 'construct_purification_step',
            },
        ),
        migrations.CreateModel(
            name='PurificationStepType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
            ],
            options={
                'db_table': 'construct_purification_step_type',
            },
        ),
        migrations.AddField(
            model_name='purificationstep',
            name='purification_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.PurificationStepType'),
        ),
        migrations.AddField(
            model_name='constructexpression',
            name='expression_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.ConstructExpressionSystem'),
        ),
        migrations.AddField(
            model_name='constructcrystallization',
            name='crystal_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construct.CrystallizationMethodTypes'),
        ),
        migrations.AddField(
            model_name='constructcrystallization',
            name='ligands',
            field=models.ManyToManyField(through='construct.ConstructCrystallizationLigandConc', to='ligand.Ligand'),
        ),
    ]
