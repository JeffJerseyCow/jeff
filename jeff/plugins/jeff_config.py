import json
from jeff.utils import updateConfig

def parser(subparsers):
    group = subparsers.add_parser('config')
    configParser = group.add_mutually_exclusive_group()
    configParser.add_argument('--show', action='store_true', help='show configuration')
    configParser.add_argument('--base-domain', type=str, help='change base domain')
    configParser.add_argument('--reset-base-domain', action='store_true', help='reset base domain')

def run(args, config):
    if args.show:
        print(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
        return True

    elif args.base_domain:
        config['baseDomain'] = args.base_domain
        updateConfig(config)
        print('Changed base domain to %s' % args.base_domain)
        return True

    elif args.reset_base_domain:
        config['baseDomain'] = ""
        updateConfig(config)
        print('Reset base domain')
        return True

    else:
        print('Error: No argument specified')
        return False
