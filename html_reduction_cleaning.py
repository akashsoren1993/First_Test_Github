import pandas as pd
import re


def cleaning_for_avoiding_json_error(cleaned_html):
    json_cleaned = re.sub(r"'", "’", cleaned_html)
    json_cleaned = re.sub(r'"', '', json_cleaned)
    return json_cleaned


def _header_body_html_cleaning(raw_html):
    header_body_raw_html = re.sub(r'\s\s\s+', " ", str(raw_html))
    header_body_raw_html = re.sub(r'\n', " ", str(header_body_raw_html))
    # header_body_raw_html = re.sub(r'<style.*style>', "", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<script.*script>', "", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<noscript.*noscript>', "", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<style.*style>', "", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'\s+\S+="[^"]*"', "", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<[^<]+?>', "<>", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<>\s<>\s*', "<>", str(header_body_raw_html))
    header_body_raw_html = re.sub(r'<', "", str(header_body_raw_html))
    header_body_raw_html_cleaned = re.sub(r'>+', ">", str(header_body_raw_html))
    header_body_raw_html_cleaned = cleaning_for_avoiding_json_error(header_body_raw_html_cleaned)
    header_body_raw_html_cleaned_length = len(header_body_raw_html_cleaned)
    return header_body_raw_html_cleaned, header_body_raw_html_cleaned_length


def _script_html_cleaning(raw_html):
    script_raw_html = re.sub(r'\s\s\s+', " ", str(raw_html))
    script_raw_html = re.sub(r'\n', " ", str(script_raw_html))
    # cleaned_html = re.sub(r'<style.*style>', "", str(script_raw_html))
    script_raw_html = re.findall(r"<script.*script>", script_raw_html)
    if len(script_raw_html) != 0:
        print("script is there")
        # cleaned_html = re.sub(r'<script.*script>', "", str(cleaned_html))
        # cleaned_html = re.sub(r'<noscript.*noscript>', "", str(cleaned_html))
        script_raw_html = re.sub(r'\s+\S+="[^"]*"', "", str(script_raw_html[0]))
        script_raw_html = re.sub(r'<[^<]+?>', "<>", str(script_raw_html))
        script_raw_html = re.sub(r'<>\s<>\s*', "<>", str(script_raw_html))
        script_raw_html = re.findall(r"<>[^<>{]+<>", script_raw_html)
        script_raw_html_cleaned = "".join(script_raw_html)
        script_raw_html_cleaned = cleaning_for_avoiding_json_error(script_raw_html_cleaned)
        script_raw_html_cleaned_length = len(script_raw_html_cleaned)
        return script_raw_html_cleaned, script_raw_html_cleaned_length
    else:
        print("script is not there")
        return "", 0


def _noscript_html_cleaning(raw_html):
    raw_html_initial_cleaning = re.sub(r'\s\s\s+', " ", str(raw_html))
    raw_html_initial_cleaning = re.sub(r'\n', " ", str(raw_html_initial_cleaning))
    raw_html_initial_cleaning = re.sub(r'<script.*script>', "", str(raw_html_initial_cleaning))
    noscript_raw_html = re.findall(r"<noscript.*noscript>", raw_html_initial_cleaning)
    if len(noscript_raw_html) != 0:
        print("noscript is there")
        noscript_raw_html = re.sub(r'\s+\S+="[^"]*"', "", str(noscript_raw_html[0]))
        noscript_raw_html = re.sub(r'<[^<]+?>', "<>", str(noscript_raw_html))
        noscript_raw_html = re.sub(r'<>\s<>\s*', "<>", str(noscript_raw_html))
        noscript_raw_html = re.sub(r'<', "", str(noscript_raw_html))
        noscript_raw_html_cleaned = re.sub(r'>+', ">", str(noscript_raw_html))
        noscript_raw_html_cleaned = cleaning_for_avoiding_json_error(noscript_raw_html_cleaned)
        noscript_raw_html_cleaned_length = len(noscript_raw_html_cleaned)
        return noscript_raw_html_cleaned, noscript_raw_html_cleaned_length
    else:
        print("noscript is not there")
        return "", 0


input = pd.read_csv("html_extraction_final.csv")

print(input.columns)
# htmls = input["html"][0]

input['body_header_cleaned'] = ""
input['body_header_cleaned_length'] = 0

input['noscript_cleaned'] = ""
input['noscript_cleaned_length'] = 0

input['script_cleaned'] = ""
input['script_cleaned_length'] = 0

for i in range(len(input["html"])):
    print("index is", i)
    main_raw_html = input["html"][i]

    body_header_raw_html_cleaned, body_header_raw_html_cleaned_length = _header_body_html_cleaning(main_raw_html)

    noscript_raw_html_cleaned, noscript_raw_html_cleaned_length = _noscript_html_cleaning(main_raw_html)
    script_raw_html_cleaned, script_raw_html_cleaned_length = _script_html_cleaning(main_raw_html)

    print("the length of all cleaned body_header, noscript and script for link {} are {}, {}, {}".format
          (input["_root"][i], body_header_raw_html_cleaned_length, noscript_raw_html_cleaned_length,
           script_raw_html_cleaned_length))
    print("---------")
    input.at[i, 'body_header_cleaned'] = body_header_raw_html_cleaned
    input.at[i, 'body_header_cleaned_length'] = body_header_raw_html_cleaned_length
    input.at[i, 'noscript_cleaned'] = noscript_raw_html_cleaned
    input.at[i, 'noscript_cleaned_length'] = noscript_raw_html_cleaned_length
    input.at[i, 'script_cleaned'] = script_raw_html_cleaned
    input.at[i, 'script_cleaned_length'] = script_raw_html_cleaned_length

input.to_csv("cleaned_htmls.csv", index=False)


