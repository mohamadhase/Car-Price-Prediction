from dataclasses import dataclass


#make the attrs not required

@dataclass()
class CarFeatures:
    """Car features dataclass"""
    car_name: str = None
    year: int   = None
    price: int  = None
    color: str  = None
    fuil_type: str = None
    car_prev_state: str = None
    license_country: str = None
    transimission_type: str = None
    glass_type: str = None
    motor_power: int = None
    mileage: int = None
    passenger_capacity: str = None
    prev_owners: str = None
    additional_info: str = None
    insurance_cost: int = None
    sell_date: str = None
    def add_feature(self, key, value):
        """this method is responsible for adding the features to the object

        Args:
            key (str): the key of the feature
            value (_type_): the value of the feature
        """
        if key == 'لون السيارة':
            self.color = value
        elif key == 'اسم السيارة':
            self.car_name = value
        elif key=='السنة':
            try:
                self.year = int(value)
            except Exception:
                self.year = None
        elif key=='السعر':
            try:
                self.price = int(value)
            except Exception:
                self.price = None
        elif key == 'نوع الوقود':
            self.fuil_type = value
        elif key == "أصل السيارة":
            self.car_prev_state = value
        elif key == 'رخصة السيارة':
            self.license_country = value
        elif key == 'نوع الجير':
            self.transimission_type = value
        elif key == 'الزجاج':
            self.glass_type = value
        elif key == 'قوة الماتور':
            try:
                self.motor_power = int(value)
            except Exception:
                self.motor_power = None
        elif key == 'عداد السيارة':
            try:
                self.mileage = int(value)
            except Exception:
                self.mileage = None
        elif key == 'عدد الركاب':
            self.passenger_capacity = value
        elif key == 'أصحاب سابقون':
            self.prev_owners = value
        elif key == 'المجموع':
            try:
                self.insurance_cost = int(value)
            except Exception:
                self.insurance_cost = None
        elif key == 'تاريخ نشر الإعلان':
            self.sell_date = value
        elif key == 'ملاحظات':
            if self.additional_info == None:
                self.additional_info = value
            else:
                self.additional_info += ","+value
        
@dataclass()
class CarFeaturesPrediction:
    """Car features dataclass"""
    car_name:str
    year: int   
    color: str  
    fuil_type: str
    car_prev_state: str 
    license_country: str 
    transimission_type: str 
    glass_type: str 
    motor_power: int
    mileage: int 
    passenger_capacity: str 
    prev_owners: str 
    additional_info: str 
    sell_date: str
