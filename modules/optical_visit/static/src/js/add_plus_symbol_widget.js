/** @odoo-module **/
import { registry } from '@web/core/registry';
import { FloatField, floatField } from '@web/views/fields/float/float_field';

export class AddPlusSymbolWidget extends FloatField {
  get formattedValue() {
    const plusSymbol = this.props.record.data[this.props.name] >= 0 ? '+' : '';
    return plusSymbol + super.formattedValue;
  }
}

registry.category('fields').add('add_plus_symbol', {
  ...floatField,
  component: AddPlusSymbolWidget,
});
