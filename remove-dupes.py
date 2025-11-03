import json


def get_settings():
    with open('settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    settings = get_settings()
    my_project_id = settings['project_name']

    with open(f'output/{my_project_id}.srt', encoding='utf-8') as subs_file:
        timings_lines = subs_file.read().split('\n\n')

    out = ''

    last = ''
    for i, t in enumerate(timings_lines):
        lines = t.split('\n')
        if len(lines) > 1:
            num = lines[0]
            timing = lines[1]
            text = lines[2:]

            first = text[0]

            # if len(text) == 0 or len(text[0]) == 0:
            #     print('empty text?')
            print(text)

            if first == last:
                print('FOUND DUPE:', first)
                text = text[1:]

                # if len(text) == 1:
                #     print('DUPE BAD')

            last = text[-1]

            # print()

            out += num + '\n'
            out += timing + '\n'
            out += '\n'.join(text)
            out += '\n\n'

            if len(text) == 0:
                breakpoint()

    print(out)



    # out = 'bla'
    with open(f'output/{my_project_id}-fixed.srt', 'w', encoding='utf-8') as out_file:
        out_file.write(out)

if __name__ == "__main__":
    main()
