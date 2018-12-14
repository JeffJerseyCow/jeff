from jeff.utils import updateConfig

def parser(subparsers):
    debugParser = subparsers.add_parser('config')
    debugParser.add_argument('-b', '--base-domain', type=str,
        help='change base domain')
    debugParser.add_argument('--reset-base-domain', action='store_true',
        help='reset base domain')

def run(args, config):
    if args.base_domain:
        config['baseDomain'] = args.base_domain
        print('[*] changed base domain to "%s"' % args.base_domain)
        updateConfig(config)

    if args.reset_base_domain:
        config['baseDomain'] = ""
        print('[*] reset base domain')
        updateConfig(config)

    return True
