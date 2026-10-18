class LZW:
    @staticmethod
    def compress(uncompressed: str) -> list:
        """Compresses a string to a list of output symbols."""
        # Build the dictionary.
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}
        
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        
        # Output the code for w.
        if w:
            result.append(dictionary[w])
        return result

    @staticmethod
    def decompress(compressed: list) -> str:
        """Decompresses a list of symbols back into a string."""
        from io import StringIO
        
        # Build the dictionary.
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        
        result = StringIO()
        w = chr(compressed.pop(0))
        result.write(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            
            result.write(entry)
            
            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            
            w = entry
        return result.getvalue()

    @staticmethod
    def compress_to_string(data: str) -> str:
        """Helper to return a string representation of compressed data (using comma separated ints)."""
        compressed = LZW.compress(data)
        return ",".join(map(str, compressed))

    @staticmethod
    def decompress_from_string(data_str: str) -> str:
        """Helper to decompress from a comma separated string of ints."""
        try:
            compressed = list(map(int, data_str.split(",")))
            return LZW.decompress(compressed)
        except Exception:
            return data_str # Return as is if not LZW formatted
