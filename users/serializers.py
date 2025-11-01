from rest_framework import serializers

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self,file):
        if not file.name.endswith(".csv"):
            raise serializer.ValidationError("only CVS file allowed")
        return file