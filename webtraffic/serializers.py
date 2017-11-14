from rest_framework import serializers
from .models import ReceivedData, SentData

class ReceivedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedData 
        fields = ('host_name','packet_size_byte', 'is_retransmitted', 'pub_date')

class SentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentData 
        fields = ('host_name','packet_size_byte', 'is_retransmitted', 'pub_date')
