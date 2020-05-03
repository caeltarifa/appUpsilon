from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
fs = FileSystemStorage(location='/var/www/nuclear/appBoson/sistema_aasana/back-end/server/uploads/fotografias')        
class TrabajadoresATS(models.Model):
    id_trabajador=models.AutoField(primary_key=True,blank=False)
    
    ci=models.IntegerField(blank=True)

    ci_extension=models.CharField(max_length=90,blank=True)
    a_paterno=models.CharField(max_length=90,blank=True)
    a_materno=models.CharField(max_length=90,blank=True)
    a_casada=models.CharField(max_length=90,blank=True)
    p_nombre=models.CharField(max_length=90,blank=True)
    s_nombre=models.CharField(max_length=90,blank=True)
    nacionalidad=models.CharField(max_length=90,blank=True)
    sexo=models.CharField(max_length=90,blank=True)
    
    id_item=models.IntegerField(blank=True)
    id_seccion=models.IntegerField(blank=True)
    id_seccionactual=models.IntegerField(blank=True)

    tipo_trabajador=models.CharField(max_length=90,blank=True)
    
    foto=models.ImageField(storage=fs) 

    correo=models.CharField(max_length=90,blank=True)
    fecha_nac=models.DateField()
    telefono=models.CharField(max_length=90,blank=True)
    celular=models.CharField(max_length=90,blank=True)
    direccion= models.CharField(max_length=90,blank=True)
    id_sueldo=models.IntegerField(blank=True)
    id_cargo=models.IntegerField(blank=True)
    activo=models.BooleanField(default=False)
    areat=models.CharField(max_length=90,blank=True)
    def __str__(self):
        return '{}/{}'.format(
            self.id_trabajador,

            self.ci,

            self.ci_extension,
            self.a_paterno,
            self.a_materno,
            self.a_casada,
            self.p_nombre,
            self.s_nombre,
            self.nacionalidad,
            self.sexo,

            self.id_item,
            self.id_seccion,
            self.id_seccionactual,

            self.tipo_trabajador,

            self.foto,

            self.correo,
            self.fecha_nac,
            self.telefono,
            self.celular,
            self.direccion,
            self.id_sueldo,
            self.id_cargo,
            self.activo,
            self.areat
            )
    class Meta:
        db_table = "trabajadores"

class CuentasATS(models.Model):
    id_cuenta=models.AutoField(primary_key=True,blank=False)
    #id_trabajador=models.IntegerField(blank=True)
    id_trabajador=models.OneToOneField(TrabajadoresATS,
        on_delete=models.PROTECT,
        primary_key=False,
        null=True,
        blank=True,
        db_column="id_trabajador")
    id_rol=models.IntegerField(blank=True)
    usuario=models.CharField(max_length=90,blank=True)
    password=models.CharField(max_length=90,blank=True)
    activo=models.BooleanField(default=False)
    resetPasswordToken= models.CharField(max_length=90,blank=True)
    resetPasswordExpires= models.DateField()
    def __str__(self):
        return '{}/{}'.format(
            self.id_cuenta,
            self.id_trabajador,
            self.usuario,
            self.password,
            self.activo,
            #self.createdAt,
            #self.updatedAt,
            self.id_rol,
            self.resetPasswordToken,
            self.resetPasswordExpires
        )
    class Meta:
        db_table = "cuentas"