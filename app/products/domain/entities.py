class Product:
    def __init__(
        self,
        name,
        description,
        availability,
        quality,
        price,
        stock,
        seller,
        manufacturer,
        categories,
        identity=None,
        part_data=None,
    ):
        self.id = identity
        self.name = name
        self.categories = categories
        self.description = description
        self.availability = availability
        self.quality = quality
        self.price = price
        self.stock = stock
        self.seller = seller
        self.manufacturer = manufacturer
        self.part_data = part_data

    @classmethod
    def from_dict(cls, adict):
        part_data = None
        if 'part_data' in adict:
            part_data = PartData.from_dict(adict.get('part_data'))
        return Product(name=adict['name'],
                       description=adict['description'],
                       categories=adict['categories'],
                       availability=adict['availability'],
                       quality=adict['quality'],
                       price=adict['price'],
                       stock=adict['stock'],
                       seller=adict['seller'],
                       manufacturer=adict['manufacturer'],
                       part_data=part_data)


class PartData:
    def __init__(self, ref_part, weight, diameter, dimension, date_of_prod,
                 num_oem, country_of_origin, volume_of_part):
        self.ref_part = ref_part
        self.weight = weight
        self.diameter = diameter
        self.dimension = dimension
        self.date_of_prod = date_of_prod
        self.num_oem = num_oem
        self.country_of_origin = country_of_origin
        self.volume_of_part = volume_of_part

    @classmethod
    def from_dict(cls, adict):
        return PartData(
            ref_part=adict['ref_part'],
            weight=adict['weight'],
            diameter=adict['diameter'],
            dimension=adict['dimension'],
            date_of_prod=adict['date_of_prod'],
            num_oem=adict['num_oem'],
            country_of_origin=adict['country_of_origin'],
            volume_of_part=adict['volume_of_part'],
        )
