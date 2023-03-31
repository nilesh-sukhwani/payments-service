def deserialize_request(
    request,
    serializer_class,
    **kwargs,
):
    """
    Validates incoming request and returns validated data.
    :param request: Request - drf request object to get incoming data from
    :param serializer_class: Type[Serializer] - drf serializer class used to validate data
    :return: validated_data: dict
    """
    data = request.data

    serializer = serializer_class(
        data=data,
        context={"request": request},
        **kwargs,
    )
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data


def serialize_response(
    instance,
    serializer_class,
    **kwargs,
):
    """
    Serialize object instance using a serializer.
    :param instance: Any - instance of object to send as json
    :param serializer_class: Type[Serializer] - drf serializer to serialize with
    :return: response_data: dict
    """

    serializer = serializer_class(instance=instance, **kwargs)
    return serializer.data
