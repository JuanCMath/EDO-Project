class ParsingException(Exception):
    def __init__ (self, message):
        self.message=message
        super().__init__(self.message)

#se inicializa una sola instancia y es la que va ejecutando las cosas en el parser
class ExceptionHandling:
    def __init__(self, expression):
        self.expression = expression
        self.Reset()

    def SafeMode(self, f, *args):
        try:
            return f(args)
            #f supuestamente seria cada funcion del parser, q en vez de llamarla directamente,
            #la llamas a traves del SafeMode
        except ParsingException as var:
            self.errors.append(var.message)
            self.PanicMode(self)

    def Display(self):
        #muestra los errores de la manera que se elija despues
        #por ahora voy a imprimirlos nada mas
        if self.errors.len()>0:
            for error in self.errors:
                print (error)

    def PanicMode(self):
        #esto si debes implementarlo tu
        #la idea seria que avanzara a traves de expression (lista de tokens)
        #hasta que llegue a un token '=' o '$'
        #vaya, q modificara el count de tokens
        #yo en mi parser lo q llevaba era un enumerator de tokens, y aqui le
        #daba move next hasta que pasara un token seguro, como ';' o '}'
        pass

    def Reset(self): self.errors = []