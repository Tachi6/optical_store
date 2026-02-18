import { FloatField, floatField } from '@web/views/fields/float/float_field';
import { registry } from '@web/core/registry';

export class AddDegreeSymbolWidget extends FloatField {
  get formattedValue() {
    return this.props.record.data[this.props.name] + 'º';
  }
}

registry.category('fields').add('add_degree_symbol', {
  ...floatField,
  component: AddDegreeSymbolWidget,
});
